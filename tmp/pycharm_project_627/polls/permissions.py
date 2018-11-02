# -*- coding:utf-8 -*-

from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsOwnerOrReadyOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
        )

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return obj.creater == request.user
        #if obj.creater == request.user:
            #if request.method == 'post' and request.method == 'get':
                #return True


class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission( self, request, view, obj ):
        if request.method in permissions.SAFE_METHODS and (obj.Creater == request.user):
            return True
        return obj.Creater == request.user

class IsVbAdminUser(IsAdminUser):
    def has_object_permission( self, request, view, obj ):
        return self.has_permission(request, view)