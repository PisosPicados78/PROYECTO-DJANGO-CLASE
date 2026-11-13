from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from soporte.models import Ticket
from .services import predecir_prioridad


class MotorIAServiceTests(TestCase):
    def test_predecir_prioridad_casos(self):
        self.assertEqual(
            predecir_prioridad('Pantalla azul en el servidor y no enciende'),
            'Alta',
        )
        self.assertEqual(
            predecir_prioridad('Olvidé mi contraseña de correo'),
            'Media',
        )
        self.assertEqual(
            predecir_prioridad('Solicito cambio de mouse y teclado'),
            'Baja',
        )
        self.assertEqual(predecir_prioridad('   '), 'Media')


class ProbarIAViewTests(TestCase):
    def test_get_probar_ia(self):
        response = self.client.get(reverse('probar_ia'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'motor_ia/probar_ia.html')

    def test_post_probar_ia_muestra_resultado(self):
        response = self.client.post(
            reverse('probar_ia'),
            {'texto': 'El servidor principal se cayó y no responde'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prioridad predicha:')
        self.assertContains(response, 'Alta')


class IntegracionTicketIATests(TestCase):
    def test_crear_ticket_asigna_prioridad_ia(self):
        User.objects.create_user(username='tester', password='secret123')
        self.client.login(username='tester', password='secret123')

        response = self.client.post(
            reverse('nuevo_ticket'),
            {
                'titulo': 'Servidor caído',
                'descripcion': 'Pantalla azul y fallo crítico en producción',
            },
        )
        self.assertRedirects(response, reverse('tickets'))
        ticket = Ticket.objects.get(titulo='Servidor caído')
        self.assertEqual(ticket.prioridad, 'Alta')
        self.assertEqual(ticket.tareas.count(), 1)
        self.assertEqual(ticket.tareas.first().prioridad, 'Alta')
