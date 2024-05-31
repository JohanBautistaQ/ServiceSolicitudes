import requests
from django.conf import settings
from rest_framework import views, status
from rest_framework.response import Response
from .models import Solicitud
from .serializers import SolicitudSerializer

class SolicitudView(views.APIView):
    def post(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario_id')
        
        user_response = requests.get(f"{settings.USER_SERVICE_URL}/usuarios/{usuario_id}/")
        if user_response.status_code != 200:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        solicitud_id = request.data.get('solicitud_id')
        try:
            solicitud = Solicitud.objects.get(pk=solicitud_id)
            if solicitud.estado != 'EN_ESPERA_DOCUMENTOS':
                return Response({'error': 'Estado no permite operación'}, status=status.HTTP_400_BAD_REQUEST)
            
           
            #Aqui se debería de llamar al endpoint de documento para almacenar la info del documento
           
            solicitud.estado = 'DOCUMENTOS_RECIBIDOS'  
            solicitud.save()

            log_data = {'accion': 'Documentos subidos', 'fecha': solicitud.fecha, 'solicitud_id': solicitud_id}
            requests.post(f"{settings.LOG_SERVICE_URL}/log/", data=log_data)

            return Response({'message': 'Operación exitosa'}, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        solicitud_id = request.query_params.get('solicitud_id')
        try:
            solicitud = Solicitud.objects.get(pk=solicitud_id)
            serializer = SolicitudSerializer(solicitud)
            return Response(serializer.data)
        except Solicitud.DoesNotExist:  
            return Response({'error': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets
class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer