from rest_framework import serializers
from .models import YouubeVideos


class YouubeVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouubeVideos
        fields = '__all__'

