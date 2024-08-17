from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync


User = get_user_model()


def send_notification (to_user_id, **fields) :
    try : 
        user = User.objects.get(id=to_user_id)
    except User.DoesNotExist:
        raise Exception('Id with this user not found !')
    
    group_name = f'notification__{user.id}'
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type' : 'notification',
            'data' : {**fields}
        }
    )