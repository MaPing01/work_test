from django.contrib.auth.models import User, Group
from rest_framework import serializers
from polls.models import *
from rest_framework.validators import UniqueValidator
from django.core.paginator import Paginator
from .auth_serializers import UserSerializer,UserRegSerializer,LoginSerializer,UserSetPasswordSerializer



#global G_creater
#global G_createtime
#G_creater = serializers.ReadOnlyField(source='creater.username')
#G_createtime = serializers.ReadOnlyField(default=None)

#
class BaseSerializer(serializers.HyperlinkedModelSerializer):
    creater = serializers.ReadOnlyField(source='creater.username')
    createtime = serializers.ReadOnlyField(default=None)
    #Id = serializers.UUIDField(default=uuid.uuid4(),read_only=True)
    class Meta:
        abstract = True

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('url' , 'username')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url' , 'name')

class CustomerSerializer(BaseSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Dialog
        fields=('Id','Callee','BeginTime','EndTime','BillTime','Duration','StartTime','CloseTime','RecordFile','RecordContextFile','CreateTime','Creater')

# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True, max_length=100)
#     password = serializers.CharField(required=True, max_length=100)
#     token = serializers.CharField(required=False, max_length=1024)
#
#     class Meta:
#         model = User
#         fields = ('id','username','password','token')
#
# class UserRegSerializer(serializers.ModelSerializer):
#
#     username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
#                                      validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
#
#     password = serializers.CharField(
#         style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
#         )
#     token = serializers.CharField(required=False, max_length=1024)
#
#
#     class Meta:
#         model = User
#         fields = ( 'username', 'password', 'token')