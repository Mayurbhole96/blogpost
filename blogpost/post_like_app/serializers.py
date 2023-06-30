from rest_framework import serializers
from .models import *

class LikeSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        exclude = ['created_at']

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    
    # likes = LikeSerializer(many=True, read_only=True)
    # id = serializers.IntegerField(required=False)

    def validate(self, data):         
        if self.instance==None and Post.objects.filter(title = data['title'], is_active__in=[True], is_deleted__in=[False]).exists():
            raise serializers.ValidationError("Record already exists")
        elif self.instance!=None:
            if self.instance.id and Post.objects.filter(title = data['title'], is_active__in=[True], is_deleted__in=[False]).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Record already exists")
        return data

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'created_at', 'author', 'is_public', 'likes_count']
        # exclude = ['created_at']
        read_only_fields = ['likes_count']

    def get_likes_count(self, obj):
        return obj.like_set.count()
    
