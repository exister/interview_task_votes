import factory

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    email = factory.Sequence(lambda n: 'email{0}@test.com'.format(n))


class LoginTestCase(APITestCase):
    url = '/api/v1/login/'

    def test_username_required(self):
        response = self.client.post(self.url, data={
            'password': '123456'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_required(self):
        response = self.client.post(self.url, data={
            'username': 'user1'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_user(self):
        response = self.client.post(self.url, data={
            'username': 'user1',
            'password': '123456'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        user = UserFactory.create(username='user1')
        user.set_password('123456')
        user.save()

        response = self.client.post(self.url, data={
            'username': 'user1',
            'password': '123456'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
