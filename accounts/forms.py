from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


# Django Forms (for HTML forms)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )


# DRF Serializers (for REST API)
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')
        
        if username_or_email and password:
            # Try to authenticate with username first
            user = authenticate(username=username_or_email, password=password)
            
            # If that fails, try to find user by email and authenticate
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include username/email and password.")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 
                 'phone_number', 'language', 'currency', 'timezone_field', 'is_email_verified')
        read_only_fields = ('username', 'is_email_verified')


class PersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('date_of_birth', 'phone_number', 'address_line1', 'address_line2', 
                 'city', 'postal_code', 'country')
        extra_kwargs = {
            'date_of_birth': {'required': False},
            'phone_number': {'required': False},
            'address_line1': {'required': False},
            'address_line2': {'required': False},
            'city': {'required': False},
            'postal_code': {'required': False},
            'country': {'required': False, 'help_text': 'ISO 3166-1 alpha-2 country code (e.g., GR, US, DE)'},
        }
    
    def validate_country(self, value):
        if value and len(value) != 2:
            raise serializers.ValidationError("Country code must be exactly 2 characters (ISO 3166-1 alpha-2)")
        return value.upper() if value else value


class BankLinkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('piraeus_customer_id', 'bank_consent_ids', 'preferred_sca_method')
        read_only_fields = ('bank_consent_ids',)
        extra_kwargs = {
            'piraeus_customer_id': {'required': True, 'help_text': 'Your Piraeus Bank customer ID'},
            'preferred_sca_method': {'required': False, 'default': 'SMS'},
        }
    
    def validate_preferred_sca_method(self, value):
        valid_methods = ['SMS', 'EMAIL', 'APP', 'PUSH']
        if value and value.upper() not in valid_methods:
            raise serializers.ValidationError(f"SCA method must be one of: {', '.join(valid_methods)}")
        return value.upper() if value else 'SMS'