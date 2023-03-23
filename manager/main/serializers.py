from rest_framework import serializers
from catalog.models import Product
from cart.models import Item
from main.models import ExportStatus,ExportMeta

class ExportMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportMeta
        fields = ['name','text']

class ExportStatusSerializer(serializers.ModelSerializer):
    export = serializers.StringRelatedField()
    meta = ExportMetaSerializer()

    class Meta:
        model = ExportStatus
        fields = ['export_id','load','price','export','meta']

class ProductSerializer(serializers.ModelSerializer):
    export_status = ExportStatusSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id','admin_image','name','price','qty','storage_icon','export_status']

class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Item
        fields = ['qty','price','product']