from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import User
from .models import Notification

def send_notification(request):
    user_id = request.GET.get("user_id")
    content = request.GET.get("content", "Test notification")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"status": "User not found"}, status=400)
    
    # Save to the database
    notification = Notification.objects.create(user=user, content=content)
    
    # Send WebSocket message
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "notify",
            "data": {"content": content, "id": notification.id}
        }
    )
    
    return JsonResponse({"status": "Notification sent."})
