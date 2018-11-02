'''from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
'''

from django.conf.urls import url,include
from rest_framework import routers
from polls.views import *
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken import views

schema_view = get_swagger_view(title='My Doc')
router = routers.DefaultRouter()
router.register(r'users', UserViewSet,base_name='user')
router.register(r'groups' , GroupViewSet,base_name='group')
router.register(r'customer', CustomerViewSet,base_name='customer')
router.register(r'course', CourseViewSet,base_name='course')
router.register(r'dialogs',DialogViewSet)
router.register(r'login',LoginViewSet,base_name='login')
router.register(r'setPassword', UserSetPasswordViewset, base_name="setPassword")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^doc/', schema_view),
    url(r'^api-token-auth/', views.obtain_auth_token),
    #url(r'^api-token-auth/', UserViewSet.as_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

