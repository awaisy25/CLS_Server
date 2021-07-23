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
        fields = ["Job", "state", "entry", "middle", "senior"]
#the serilaizer that will run the validations for our calculations

class CalculateSerializer(serializers.Serializer):
    Job_ID = serializers.IntegerField()
    University_ID = serializers.IntegerField()
    State = serializers.CharField(max_length=30, allow_blank=True, allow_null=True, default=None)
    Budget = serializers.FloatField()
    Job = serializers.SerializerMethodField('get_job_object')
    University = serializers.SerializerMethodField('get_unv_object')
    Years = serializers.IntegerField(max_value=6, min_value=1)
    Percent_income = serializers.FloatField(max_value=100, min_value=1)
    Interest_rate = serializers.FloatField(max_value=50, min_value=1)
    In_state = serializers.BooleanField(default=False)

    #method to get the job data based on the Job_ID passed in. Share the serialized data
    def get_job_object(self, obj):
        job_id = obj['Job_ID']
        job_data = Job.objects.get(id=job_id)
        #print(JobSerializer(job_data).data)
        return JobSerializer(job_data).data
    #method to get the university data based on the University_ID passed in. Share the serialized data
    def get_unv_object(self, obj):
        unv_id = obj['University_ID']
        unv_data = University.objects.get(id=unv_id)
        return UniversitySerializer(unv_data).data
    
    #def get_salary_object(self, ob)



