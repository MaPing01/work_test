#from django.test import TestCase
#from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,URLPatternsTestCase,APIRequestFactory
from django.urls import include, path, reverse
from polls.models import Course
from polls.views import *
from rest_framework.test import APIClient
from django.test.client import Client
from django.views.decorators.csrf import csrf_exempt


# Create your tests here.
class CourseTests(APITestCase):
    #urlpatterns = [
        #path('', include('polls.urls')),
    #]
    client = Client()
    client.login(username='admin', password='admin123')
    def test_get_course( self ):
        client = APIClient()
        client.login(username='admin', password='admin123')
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.logout()

    def test_get_customer( self ):
        client = Client()
        client.login(username='admin1', password='admin123')
        response = self.client.get('/customer/',)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.logout()

    def test_get_course_detail( self ):
        client = Client()
        client.login(username='admin', password='admin123')
        response = self.client.get('/course/3/',)
        self.assertEqual(response.data,{'cname':'java','score':90})
        client.logout()

    def test_create_course( self ):
        #url = 'http://192.168.3.146:8230/course/'
        data = {'cname': 'DabApps','score':90}
        response = self.client.post('/course/',data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().name, 'DabApps')


