from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timezone
from .utils import check_display_vitals

@api_view(['GET'])
def ping(request):

    vitals = check_display_vitals()

    return Response({
        "status": "success",
        "message": "Pong!",
        "vitals": vitals,
        "timestamp": datetime.now(timezone.utc)
    })
