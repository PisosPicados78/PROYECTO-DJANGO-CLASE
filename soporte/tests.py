from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Tarea, Ticket


class SoporteViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='soporte_user', password='password123')
        self.ticket = Ticket.objects.create(
            titulo='Caída de red',
            descripcion='Fallo crítico en switch central',
            prioridad='Alta',
        )
        Tarea.objects.create(
            ticket=self.ticket,
            descripcion='Revisar puerto troncal',
            prioridad='Alta',
        )

    def test_home_kpis_y_acerca_de(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_tickets'], 1)
        self.assertEqual(response.context['tickets_alta'], 1)
        self.assertEqual(response.context['total_tareas'], 1)
        self.assertContains(response, '/static/css/styles.css')

        acerca = self.client.get(reverse('acerca_de'))
        self.assertEqual(acerca.status_code, 200)

    def test_vistas_protegidas_requieren_login(self):
        for name, kwargs in [
            ('tickets', {}),
            ('nuevo_ticket', {}),
            ('detalle_ticket', {'id': self.ticket.id}),
            ('editar_ticket', {'id': self.ticket.id}),
            ('crear_tarea', {'ticket_id': self.ticket.id}),
        ]:
            res = self.client.get(reverse(name, kwargs=kwargs))
            self.assertEqual(res.status_code, 302)

    def test_flujo_autenticado_soporte(self):
        self.client.login(username='soporte_user', password='password123')

        res_list = self.client.get(reverse('tickets'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, 'Caída de red')
        self.assertContains(res_list, '1 tarea')

        res_new = self.client.get(reverse('nuevo_ticket'))
        self.assertEqual(res_new.status_code, 200)

        res_detail = self.client.get(reverse('detalle_ticket', kwargs={'id': self.ticket.id}))
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, 'Prioridad asignada por IA: Alta')
        self.assertContains(res_detail, 'Revisar puerto troncal')

        res_edit = self.client.get(reverse('editar_ticket', kwargs={'id': self.ticket.id}))
        self.assertEqual(res_edit.status_code, 200)

        res_task = self.client.post(
            reverse('crear_tarea', kwargs={'ticket_id': self.ticket.id}),
            {'descripcion': 'Reiniciar servicio DHCP', 'prioridad': 'Media'},
        )
        self.assertRedirects(res_task, reverse('detalle_ticket', kwargs={'id': self.ticket.id}))
        self.assertEqual(self.ticket.tareas.count(), 2)
