# from rest_registration.api.serializers import DefaultRegisterUserSerializer
# from rest_framework import serializers
# from django.utils import timezone


# class UsernameField(serializers.Field):

#     def to_representation(self, value):
#         return super().to_representation(value)
    
#     def to_internal_value(self, data):
#         return f'{data} {timezone.now()}'



# class CustomUserRegisterSerializer(DefaultRegisterUserSerializer):

#     username = UsernameField()
    
        