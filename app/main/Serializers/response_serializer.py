from rest_framework import serializers
from ..models import *


class AccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id','Username','current_domain','domain_mask','status']

class DomainWithoutServerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id','Username','current_domain','domain_mask','status']


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'


class SiteSerializer(serializers.ModelSerializer):
    domain_name = DomainWithoutServerSerializers(many=True)
    server = ServerSerializer(many=True)

    class Meta:
        model = Site
        fields = "__all__"
