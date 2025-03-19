from rest_framework import serializers
from ..models import *


class VebmasterSerializator(serializers.ModelSerializer):
    class Meta:
        model = Vebmaster
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_url']


class SiteSerializer(serializers.ModelSerializer):
    photo_1 = ImageSerializer(allow_null=True)
    photo_about_2 = ImageSerializer(allow_null=True)
    photo_about_3 = ImageSerializer(allow_null=True)
    id_vebmaster = VebmasterSerializator(allow_null=True)

    class Meta:
        model = Site
        fields = "__all__"
