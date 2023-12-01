from django.shortcuts import render
from .models import Updateinfo
from .serializers import UpdateinfoSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from user_auth_api.views import JWTAuthentication
# Create your views here.


class UpdateinfoViewSet(viewsets.ModelViewSet):
    queryset = Updateinfo.objects.all()
    serializer_class = UpdateinfoSerializer
    authentication_classes = (JWTAuthentication, )

    @action(methods=["get"], detail=False, url_path="updateinfo", url_name="updateinfo")
    def updateinfoByAppName(self, request, *args, **kwargs):
        app_name = self.request.query_params.get('AppName', '')
        print(app_name)
        queryset = Updateinfo.objects.filter(app_name=app_name)
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)