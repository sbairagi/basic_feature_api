from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from .serializers import YouubeVideosSerializer
from .models import YouubeVideos
from rest_framework import viewsets

# Create your views here.




class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    
    # max_page_size = 25


class YouubeVideosViewSet(viewsets.ModelViewSet):
    queryset = YouubeVideos.objects.all().order_by('-id')
    serializer_class = YouubeVideosSerializer
    pagination_class = LargeResultsSetPagination