from rest_framework import serializers

from djongo import models

from .models import Form


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('fields', )
