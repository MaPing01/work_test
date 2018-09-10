'''from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello polls")'''

from django.contrib.auth.models import User,Group
from rest_framework import viewsets,status
from rest_framework import filters
from polls.serializers import UserSerializer , GroupSerializer, CustomerSerializer, CourseSerializer,DialogSerializer,\
    LoginSerializer,UserRegSerializer,UserSetPasswordSerializer
from polls.models import *
from rest_framework import permissions
from polls.permissions import IsOwnerOrReadyOnly
import json
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication,BasicAuthentication
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import BasicAuthentication
from rest_framework import mixins
from rest_framework.response import Response
from django.contrib.auth.backends import ModelBackend



class UserViewSet(viewsets.ModelViewSet,):
    '''user'''
    queryset = User.objects.all()
    ordering_fields = ('date_joined',)
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserSerializer
#重写create方法,给密码加密，并查询和创建token
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        passwd = request.data['password']
        staff = request.data['is_staff']
        user = self.perform_create(serializer)
        #给密码加密
        user.set_password(passwd)
        user.save()

        # if int(staff) > 1:
        #查询和创建token
        token = Token.objects.get_or_create(user=user)


        serializer = UserRegSerializer({'id': user.id, 'username': user.username,'is_staff':user.is_staff,'token': token[0]})
        serializer.data["status"] = status.HTTP_201_CREATED
        #headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data['password'] is not None:
            pwd = request.data['password']
            instance.set_password(pwd)
        request.data['password'] = instance.password
        # if request.data['password'] is not None:
        #     pwd = request.data['password']
        #     instance.set_password(pwd)
        # request.data['passeord'] = instance.password
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


    def perform_create(self, serializer):
        return serializer.save()

class GroupViewSet(viewsets.ModelViewSet):
    '''Group'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class LoginViewSet(viewsets.ModelViewSet):
    '''login'''
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                print (user)
                # 登录时，创建新的token
                tokenobj = Token.objects.update_or_create(user=user)
                token = Token.objects.get(user=user)
                serializer = LoginSerializer({'id': user.id, 'username': user.username,'password':'','token': token.key})
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

class UserSetPasswordViewset(viewsets.ModelViewSet):
    """
        实现用户修改密码
        输入username、password，验证正确返回password 修改成功，否则返回HTTP_400_BAD_REQUEST
    """

    serializer_class = UserSetPasswordSerializer
    #设置对象集
    queryset = User.objects.all()
    # 因修改密码只需post方法，可重写create方法，取消原有保存对象逻辑，加入修改密码逻辑
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #取出已验证的用户对象
            instance = serializer.validated_data['user']
            #设置加密密码
            instance.set_password(request.data['newpassword'])
            #保存
            instance.save()
            return Response({'status': 'password 修改成功'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

class CustomerViewSet(viewsets.ModelViewSet):
    '''customer'''
    queryset = Customer.objects.all().filter(age__gte=2)
    serializer_class = CustomerSerializer
    # permission_classes = (IsOwnerOrReadyOnly,)
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (BasicAuthentication,TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    def perform_create(self, serializer):
        serializer.save(creater=self.request.user,)
    def get_queryset(self):
        qs = Customer.objects.all()
        qs = qs.filter(age=1)       # it's ok
        fage = self.request.query_params.get('age',2)
        if fage is not None:
            qs = qs.filter(age=fage)
        return qs

class CourseViewSet(viewsets.ModelViewSet,):
    '''course'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('cname',)
    def perform_create(self, serializer):
        serializer.save(creater=self.request.user,)

class DialogViewSet(viewsets.ModelViewSet,):
    queryset =Dialog.objects.all()
    serializer_class = DialogSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadyOnly,)
    def create(self, request, *args, **kwargs):
        newdata = self.analysis_cdr(request.data)
        serializer = self.get_serializer(data=newdata)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("ok", status=status.HTTP_200_OK, headers=headers)

    def perform_create( self, serializer ):
        serializer.save(Id=self.id)

    def analysis_cdr(self,cdr):
        if  cdr and  'cdr' in cdr:
            vd = json.loads (cdr['cdr'])
            data_dict = {}
            self.id=vd["variables"]["uuid"]
            data_dict["Id"] = vd["variables"]["uuid"]
            data_dict["Callee"] = vd["variables"]["sip_to_user"]
            data_dict["BeginTime"] = vd["variables"]["answer_stamp"]
            data_dict["EndTime"] = vd["variables"]["end_stamp"]
            data_dict["BillTime"] =  vd["variables"]["billsec"]
            data_dict["Duration"] =  vd["variables"]["duration"]
            data_dict["StartTime"] = vd["variables"]["start_stamp"]
            data_dict["CloseTime"] = vd["variables"]["end_stamp"]
            #data_dict["RecordFile"] =vd["variables"]["uuid"]+".wav"
            #data_dict["RecordContextFile"] =vd["variables"]["uuid"]+".json"
            data_dict["CreateTime"] =datetime.datetime.now()
            return data_dict
        return  cdr

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Dialog.objects.get(pk=request.query_params["uuid"])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update( self, serializer ):
        serializer.save()


# class DilogCdr(generics.CreateAPIView):
#     serializer_class=DialogSerializer
#
#     def post(self, request, *args, **kwargs):
#         newdata=self.analysis_cdr(request.data)
#         serializer = self.get_serializer (data=newdata)
#         serializer.is_valid (raise_exception=True)
#         self.perform_create (serializer)
#         headers = self.get_success_headers (serializer.data)
#         return Response ("ok", status=status.HTTP_200_OK, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save(Id=self.id)
#
#     def analysis_cdr(self,cdr):
#         if  cdr and  'cdr' in cdr:
#             vd = json.loads (cdr['cdr'])
#             data_dict = {}
#             self.id=vd["variables"]["uuid"]
#             data_dict["Id"] = vd["variables"]["uuid"]
#             data_dict["Callee"] = vd["variables"]["sip_to_user"]
#             data_dict["BeginTime"] = vd["variables"]["answer_stamp"]
#             data_dict["EndTime"] = vd["variables"]["end_stamp"]
#             data_dict["BillTime"] =  vd["variables"]["billsec"]
#             data_dict["Duration"] =  vd["variables"]["duration"]
#             data_dict["StartTime"] = vd["variables"]["start_stamp"]
#             data_dict["CloseTime"] = vd["variables"]["end_stamp"]
#             #data_dict["RecordFile"] =vd["variables"]["uuid"]+".wav"
#             #data_dict["RecordContextFile"] =vd["variables"]["uuid"]+".json"
#             data_dict["CreateTime"] =datetime.datetime.now()
#             return data_dict
#         return  cdr
#
# class DilogRecord(generics.CreateAPIView,generics.UpdateAPIView):
#     serializer_class=DialogSerializer
#     queryset = Dialog.objects.all ()
#     def post(self,request,*args,**kwargs):
#         #self.patch(request,args,kwargs)
#        return self.patch(request,args,kwargs)
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop ('partial', False)
#         instance = Dialog.objects.get(pk=request.query_params["uuid"])
#         serializer = self.get_serializer (instance, data=request.data, partial=partial)
#         serializer.is_valid (raise_exception=True)
#         self.perform_update (serializer)
#
#         if getattr (instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#
#         return Response (serializer.data)
#
#     def perform_update(self, serializer):
#         serializer.save()