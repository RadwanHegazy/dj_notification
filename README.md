# Django Rest Framework Notification Package 
This is a python package that is compatible with django to create real-time notifications.


## Some notes before use this package
- this package only works on django rest frameowork
- this package only support only jwt
- the data which is send in the consumer is flexable

## Installation

```
git clone https://github.com/RadwanHegazy/dj-notificaiton
```
```
pip install -r dj_notification/dj_notification_requirements.txt 
```

## Integrate with django


```python
# your_project/settings.py

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'daphne', # NOTE: but daphne in the top of the apps
    'dj_notification',
]

ASGI_APPLICATION = 'PROJECT_NAME.asgi.application'


# NOTE: don't use this option in production mode !
# you can use redis in production mode
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}


# Set authentication class to JWTAuthentication
# NOTE: it's important to use dj_notification
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```


```python

# your_project/asgi.py
import os
from dj_notification.middlewares import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from dj_notification.consumer import NotificationConsumer
from django.urls import path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PROJECT_NAME.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter([
                
                # this is the websocket notification path
                path('ws/notification/', NotificationConsumer.as_asgi()), 
            
            ])),
        ),
    }
)

```

## Let's Try our package !

```python
# your_app/views.py

from dj_notification.notify import send_notification
from django.http import HttpResponse

def index (request) : 
    """
    In this custom view we use send_notification method 
    to send notification to all users.
    """
    users = User.objects.all()
    for user in users : 
        send_notification(
            to_user_id=user.id,
            title='Notification Title',
            body='Notification Body',
            # feel free to write more kwargs here !
        )
    return HttpResponse('msgs sends to all users')


# your_app/urls.py
urlpatterns = [
    path('', index)
]

```

# This is all about the package and you can depend on this package in your projects to implement real-time notification to your systems.