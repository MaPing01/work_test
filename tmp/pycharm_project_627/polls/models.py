# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#为每个用户添加token验证
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#Create your models here.
# global G_creater
# global G_createtime
# G_creater = models.ForeignKey('auth.User',on_delete=True)
# G_createtime = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

class BaseModel(models.Model):
    #Id = models.UUIDField(primary_key=True,default=uuid.uuid4(),editable=False)
    creater = models.ForeignKey('auth.User', on_delete=True)
    createtime = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    class Meta:
        abstract = True

class Customer(BaseModel):
    name =  models.CharField('客户姓名',max_length=10,unique=True,null=True)
    phone = models.CharField('电话',max_length=30,unique=True,null=True)
    age=models.IntegerField(verbose_name='年龄',default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customer'

class Course(BaseModel):
    cname =  models.CharField('课程',max_length=10,unique=True,null=True)
    score = models.IntegerField('成绩',unique=False,null=True)

    def __str__(self):
        return self.cname

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'course'

class Dialog(models.Model):
    Id = models.UUIDField (primary_key=True, default=uuid.uuid4 (),editable=False)
    Callee=models.CharField(max_length=15,blank=False,default='',verbose_name='被叫号码')
    BeginTime=models.DateTimeField(default=None,verbose_name='开始时间')
    EndTime = models.DateTimeField (default=None, verbose_name='结束时间')
    BillTime=models.IntegerField(default=0,verbose_name='计费时长')
    Duration=models.IntegerField(default=0,verbose_name='通话时长')
    StartTime=models.DateTimeField(default=None,verbose_name='拨打时间')
    CloseTime=models.DateTimeField(default=None,verbose_name='挂断时间')
    #Bot=models.ForeignKey (Bot, related_name='dialog_bot',blank=False,null=True,default=None,verbose_name='机器人',on_delete=models.SET_NULL)
    #Scence=models.ForeignKey (Scence, related_name='dialog_bot',blank=False, null=True, default=None, verbose_name='场景',on_delete=models.SET_NULL)
    #Line=models.ForeignKey (Line, related_name='dialog_bot',blank=False, null=True, default=None, verbose_name='线路',on_delete=models.SET_NULL)
    #Customer=models.ForeignKey(Customer,related_name='dialog_bot',blank=True,null=True,verbose_name='被叫客户',on_delete=models.SET_NULL)
    RecordFile=models.FileField(blank=True,null=True,upload_to="dialogRecord", verbose_name='对话录音文件')
    RecordContextFile=models.FileField(blank=True,null=True,upload_to='dialogContext',verbose_name='对话内容文件')
    Creater = models.ForeignKey (User, related_name='dialog_creater', default=None,null=True, verbose_name='创建人',
                                   on_delete=models.SET_NULL)
    CreateTime = models.DateTimeField (default=timezone.now, verbose_name='创建时间')

# class AccessControl(models.Model):
#     """
#     自定义权限控制
#     """
#     class Meta:
#         permissions = (
#             ('access_dashboard', '控制面板'),
#             ('access_log', '日志管理'),
#             ('access_role_manage', '角色管理'),
#             ('access_user_manage', '用户管理'),
#         )

class AccessControl(models.Model):
    class Meta:
        permissions= (
            ('access_role_manage',u'role'),
        )