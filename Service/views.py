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
            email = solicitud.emailUser
            
            user_response = requests.get(f"{settings.USER_SERVICE_URL}/cliente/{email}/")
            if user_response.status_code != 200:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            
            doc_response = next((doc for doc in documents if doc['id'] == solicitud_id), None)
            if not doc_response:
                return Response({'error': 'Documentos no encontrados para esta solicitud'}, status=status.HTTP_404_NOT_FOUND)

            documentos = doc_response['documentos']
            
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
































documents = [
    {"id": "1", "documentos": [
        {"tipo": "PDF", "url": "http://example.com/doc1.pdf", "score": 85},
        {"tipo": "JPEG", "url": "http://example.com/doc1.jpg", "score": 70}
    ]},
    {"id": "2", "documentos": [
        {"tipo": "DOCX", "url": "http://example.com/doc2.docx", "score": 90},
        {"tipo": "PNG", "url": "http://example.com/doc2.png", "score": 75}
    ]}
]