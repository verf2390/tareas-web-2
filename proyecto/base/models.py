from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    usuario = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='tareas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completo = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    fecha_tarea = models.DateTimeField(null=True, blank=True)  # <-- NUEVO

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['completo']
