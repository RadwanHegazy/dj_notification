from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(decoded_token):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import AnonymousUser
    try:
        user = get_user_model().objects.get(id=decoded_token["user_id"])
        return user
   
    except get_user_model().DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
        
    async def __call__(self, scope, receive, send, *args, **kwargs):
        close_old_connections()
        
        token = dict(scope)['query_string'].decode('utf-8').split('=')[-1]

        if token is None or token == '':
            from django.contrib.auth.models import AnonymousUser
            return await self.inner(dict(scope, user=AnonymousUser()), receive, send, *args, **kwargs)
        from rest_framework_simplejwt.tokens import UntypedToken

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = await get_user(decoded_data)
            if user.is_authenticated:
                return await self.inner(dict(scope, user=user), receive, send, *args, **kwargs)
            return None