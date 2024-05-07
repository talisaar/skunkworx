from rest_framework import serializers
from homepage.models import myUser

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = myUser
        fields = ["username", "first_name", "last_name", "email", "password"]