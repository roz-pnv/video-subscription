from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        required=True,
        validators=[validate_password],
    )

    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Password fields add not match.'})
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user
    

class SignUpSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'national_id',
            'phone',
            'birthdate',
            'description',
            'is_admin',
        ]
    
    
    is_admin = serializers.BooleanField(
        required=False,
        label='Sign-up as admin',
        initial=False,
    )


    def create(self, validated_data):
        user_data = validated_data['user']
        user = UserSerializer.create(UserSerializer(), user_data)
        userprofile = Profile.objects.create(
            user=user,
            national_id=validated_data['national_id'],
            phone=validated_data['phone'],
            birthdate=validated_data['birthdate'],
            description=validated_data['description'],
            is_admin=validated_data['is_admin'],
        )

        userprofile.save()

        return userprofile
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    username = serializers.CharField(required=True, validators=[])
    
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': 'Email already taken.'})

        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({'username': 'Username already taken.'})

        return value
    
    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        return user
    

class UpdateProfileSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()
    class Meta:
        model = Profile
        fields = [
            'user',
            'national_id',
            'phone',
            'birthdate',
            'description',
            'is_admin',
        ]

    is_admin = serializers.BooleanField(
        required=False,
        label='Sign-up as admin',
        initial=False,
    )

    def create(self, validated_data):
        user_data = validated_data['user']
        username = user_data.get('username')

        user = User.objects.filter(username=username).first()
        profile, created = Profile.objects.get_or_create(user_id=user.id)
        
        user = UpdateUserSerializer.create(UpdateUserSerializer() ,user_data)
       
        profile.national_id=validated_data['national_id']
        profile.phone=validated_data['phone']
        profile.birthdate=validated_data['birthdate']
        profile.description=validated_data['description']
        profile.is_admin=validated_data['is_admin']
        profile.save()

        return profile


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'oldpassword',
            'password',
            'password2',
        ]
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    password2 = serializers.CharField(write_only=True, required=True)
    oldpassword = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Password fields add not match.'})
        
        return data

    def validate_oldpassword(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password is not correct.'})

        return value
    
    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
