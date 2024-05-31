import requests
from django.conf import settings
from rest_framework import views, status
from rest_framework.response import Response
from .models import Solicitud
from .serializers import SolicitudSerializer

class SolicitudView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        solicitud_id = request.query_params.get('id')

        try:
            solicitud = Solicitud.objects.get(pk=solicitud_id)
            print(solicitud_id)
            print(solicitud)
            email = solicitud.emailUser 
            
            user_response = requests.get(f"{settings.USER_SERVICE_URL}/cliente/{email}/")
            if user_response.status_code != 200:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            print(user_response.json())
            doc_response = requests.get(f"{settings.DOCUMENT_SERVICE_URL}/documentos/{solicitud_id}/")
            if doc_response.status_code != 200:
                return Response({'error': 'Documentos no encontrados para esta solicitud'}, status=status.HTTP_404_NOT_FOUND)

            documentos_data = doc_response.json()
            documentos = documentos_data.get('documentos', [])
            
            return Response({
                'solicitud': SolicitudSerializer(solicitud).data,
                'documentos': [{
                    'tipo': doc['tipo'],
                    'url': doc['url'],
                    'score': doc['score']
                } for doc in documentos]
            }, status=status.HTTP_200_OK)

        except Solicitud.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)

