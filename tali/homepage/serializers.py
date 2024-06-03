from rest_framework import serializers
from homepage.models import myUser, Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = myUser
        fields = ["username", "first_name", "last_name", "email", "password", "posts", "id"]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Post
        fields = ["id","owner", "created", "content", "id"]
