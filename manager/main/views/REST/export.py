from rest_framework import viewsets
from rest_framework import permissions
from main.serializers import ExportStatusSerializer
from main.models import ExportStatus
from django.shortcuts import get_object_or_404

class ExportStatusViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = ExportStatus.objects.filter(product__id=pk)
        export_status = get_object_or_404(queryset, pk=pk)
        serializer = ExportStatusSerializer(export_status)

        return Response(serializer.data)