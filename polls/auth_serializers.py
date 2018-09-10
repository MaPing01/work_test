from rest_framework import  serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework.compat import authenticate



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('url' , 'username','is_staff')


class UserRegSerializer(serializers.ModelSerializer):

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
        )
    is_staff = serializers.CharField(label="是否员工", help_text="是否员工", required=True, allow_blank=False,)
    token = serializers.CharField(required=False, max_length=1024)

    class Meta:
        model = User
        fields = ( 'username', 'password', 'is_staff', 'token')


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)
    token = serializers.CharField(required=False, max_length=1024)

    class Meta:
        model = User
        fields = ('id','username','password','token')


class UserSetPasswordSerializer(serializers.ModelSerializer):

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False)
    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码", write_only=True,
        )
    newpassword = serializers.CharField(
        style={'input_type': 'password'}, help_text="新密码", label="新密码", write_only=True,
    )

    # 验证用户名、密码是否正确
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # 用户名称、密码登录验证
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)

            if not user:
                msg = '不能修改'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = '必须输入同时输入名称和密码'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    class Meta:
        model = User
        fields = ('username', 'password', 'newpassword')