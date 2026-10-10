from django.db import models

class Ticket(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='tickets/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Tarea(models.Model):
    PRIORIDAD_CHOICES = [
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ]

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='Media')

    def __str__(self):
        return self.descripcion
