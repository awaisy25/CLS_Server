from rest_framework import serializers
from .models import Job, University, Salary

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "title"]

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "in_state", "out_state"]


class SalarySerializer(serializers.ModelSerializer):
    #retrieivng the job title from job serializer. Source matches it by job_id
    Job = JobSerializer(source="job", read_only=True)
    class Meta:
        model = Salary
        fields = ["id", "Job", "state", "entry", "middle", "senior"]


