from django.db import models

class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('CANCELADA', 'Cancelada'),
        ('EN_ESPERA_DOCUMENTOS', 'En espera de documentos'),
        ('OFERTA_CREADA', 'Oferta creada'),
        ('OFERTA_ACEPTADA', 'Oferta aceptada'),
        ('FINALIZADO', 'Finalizado'),
        ('EN_ESPERA_OFERTAS', 'En espera de ofertas'),
        ('DOCUMENTOS_RECIBIDOS', 'Documentos recibidos'),
    ]

    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='EN_ESPERA_DOCUMENTOS')
    fecha = models.DateField(auto_now_add=True)
    meta_dato_id = models.IntegerField() 
