from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin_user', password='password123')
        self.grupo = Group.objects.create(name='Nivel 1')

    def test_login_y_registro_render(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)
        self.assertEqual(self.client.get(reverse('registro')).status_code, 200)

        res = self.client.post(
            reverse('login'),
            {'username': 'admin_user', 'password': 'password123'},
        )
        self.assertRedirects(res, reverse('home'))

    def test_gestion_grupos_autenticado(self):
        self.assertEqual(self.client.get(reverse('grupos')).status_code, 302)

        self.client.login(username='admin_user', password='password123')
        res = self.client.get(reverse('grupos'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Nivel 1')

        res_edit = self.client.post(
            reverse('editar_grupo', kwargs={'id': self.grupo.id}),
            {'name': 'Nivel 2'},
        )
        self.assertRedirects(res_edit, reverse('grupos'))
        self.grupo.refresh_from_db()
        self.assertEqual(self.grupo.name, 'Nivel 2')
