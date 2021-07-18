from rest_framework import serializers
from .models import Job, University

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "title"]

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "in_state", "out_state"]



