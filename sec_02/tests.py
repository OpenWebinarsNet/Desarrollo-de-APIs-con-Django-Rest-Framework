# myApp/test.py
from datetime import date
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Resource, Booking

class BookingAPITest(APITestCase):
    fixtures = ['user', 'resource', 'booking']

    def _authenticate(self):
        # self.client.login(username='admin', password='admin') # BasicAuthentication
        # my_user = User.objects.create_user('admin', password='admin')
        my_user = User.objects.get(id=1)
        token = Token.objects.create(user=my_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_booking(self):
        response = self.client.get('/api/booking/')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 2)
        self.assertIsInstance(response_json, list)
        self.assertIsInstance(response_json[0], dict)
        self.assertIsInstance(response_json[1], dict)
    
    def test_get_one_booking(self):
        response = self.client.get('/api/booking/1/')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 9)
        self.assertIsInstance(response_json.get('user'), int)
        self.assertIsInstance(response_json.get('resource'), int)
        self.assertIsInstance(response_json.get('start_date'), str)
        self.assertIsInstance(response_json.get('end_date'), str)
        self.assertIsInstance(response_json.get('start_time'), str)
        self.assertIsInstance(response_json.get('end_time'), str)
        self.assertIsInstance(response_json.get('status'), str)

    def test_post_booking(self):
        url = '/api/booking/'
        data =   {
            "start_date": "2023-10-02",
            "end_date": "2023-10-02",
            "start_time": "04:45:00",
            "end_time": "06:47:00",
            "status": "SO",
            "_order": 0,
            "user": 2,
            "resource": 1
        }
        self.client.login(username='admin', password='admin') # BasicAuthentication
        response = self.client.post(url, data, format='json')
        # response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 3)
        self.assertEqual(Booking.objects.all().last().status, 'SO')
        self.assertEqual(Booking.objects.all().last().user.pk, 2)
        self.assertEqual(Booking.objects.all().last().resource.pk, 1)
        self.assertEqual(Booking.objects.all().last().start_date, date(2023, 10, 2))
    
    def test_put_booking(self):
        url = '/api/booking/1/'
        data =     {
            "id": 1,
            "start_date": "2023-12-02",
            "end_date": "2023-12-02",
            "start_time": "00:00:00",
            "end_time": "00:00:00",
            "status": "SO",
            "_order": 0,
            "user": 2,
            "resource": 2
        }
        self.client.login(username='admin', password='admin') # BasicAuthentication
        response = self.client.put(url, data, format='json')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.objects.count(), 2)
        self.assertEqual(Booking.objects.get(id=1).status, 'SO')
        self.assertEqual(Booking.objects.get(id=1).user.pk, 2) # Clave foránea
        self.assertEqual(Booking.objects.get(id=1).resource.pk, 2) # Clave foránea
        self.assertEqual(Booking.objects.get(id=1).start_date, date(2023, 12, 2))
    
    def test_delete_booking(self):
        self.client.login(username='admin', password='admin') # BasicAuthentication
        response = self.client.delete('/api/booking/1/')
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 1)

    def test_get_resources(self):
        self.client.login(username='admin', password='admin') # BasicAuthentication
        response = self.client.get('/api/resources/')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 2)
        self.assertIsInstance(response_json, list)
        self.assertIsInstance(response_json[0], dict)
        self.assertIsInstance(response_json[1], dict)

    def test_get_one_resource(self):
        self.client.login(username='admin', password='admin') # BasicAuthentication
        response = self.client.get('/api/resources/1/')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 4)
        self.assertIsInstance(response_json.get('name'), str)
        self.assertIsInstance(response_json.get('description'), str)
        self.assertIsInstance(response_json.get('type'), str)
    
    def test_post_resource(self):
        url = '/api/resources/'
        data =  {
            "name": "Sala de reuniones principal",
            "description": "Sala de 40 metros cuadrados, 25 sillas y mesa central.",
            "type": "MA"
        }
        self.client.login(username='admin', password='admin') # BasicAuthentication
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resource.objects.count(), 3)
        self.assertEqual(Resource.objects.all().last().name, 'Sala de reuniones principal')
        self.assertEqual(Resource.objects.all().last().type, 'MA')


    def test_get_users(self):
        self._authenticate() # TokenAuthentication
        response = self.client.get('/api/users/')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response_json, list)
        self.assertIsInstance(response_json[0], dict)
        self.assertIsInstance(response_json[1], dict)

    def test_get_one_user(self):
        self._authenticate() # TokenAuthentication
        response = self.client.get('/api/users/1/')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_json), 5) # número de campos
        self.assertEqual(response_json.get('username'), 'admin')
        self.assertEqual(response_json.get('is_staff'), True)

    def test_post_user(self):
        url = '/api/users/'
        data = {
            "username": "editor",
            "password": "editor"
        }
        self._authenticate() # TokenAuthentication
        
        response = self.client.post(url, data, format='json')
        response_json = response.json()
        # print(response_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)

    
    
