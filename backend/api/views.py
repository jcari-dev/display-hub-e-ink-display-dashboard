from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timezone

@api_view(['GET'])
def ping(request):
    return Response({
        "status": "success",
        "message": "Pong!",
        "timestamp": datetime.now(timezone.utc)
    })
