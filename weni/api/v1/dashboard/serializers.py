from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from weni.common.models import Newsletter, ServiceStatus, Service, Organization


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["id", "title", "description", "created_at"]
        ref_name = None


class StatusServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceStatus
        fields = [
            "id",
            "project",
            "service__status",
            "service__url",
            "service__default",
            "service__last_updated",
            "service__type_service",
            "created_at",
        ]
        ref_name = None

    service__status = serializers.BooleanField(source="service.status")
    service__url = serializers.CharField(source="service.url")
    service__default = serializers.BooleanField(source="service.default")
    service__last_updated = serializers.DateTimeField(source="service.last_updated")
    service__type_service = serializers.ChoiceField(
        choices=Service.SERVICE_TYPE_CHOICES,
        default=Service.SERVICE_TYPE_CHAT,
        label=_("Type Service"),
        source="service.service_type",
        read_only=True,
    )
