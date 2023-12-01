from rest_framework import serializers
from .models import Updateinfo



class UpdateinfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Updateinfo
        fields = '__all__'