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
    State = serializers.CharField(max_length=30, allow_blank=True, allow_null=True, default="US")
    Budget = serializers.FloatField()
    Job = serializers.SerializerMethodField('get_job_object')
    University = serializers.SerializerMethodField('get_unv_object')
    Loan_total = serializers.SerializerMethodField('get_loan_total')
    Years = serializers.IntegerField(max_value=6, min_value=1)
    Percent_income = serializers.FloatField(max_value=100, min_value=1, default=20)
    Interest_rate = serializers.FloatField(max_value=50, min_value=1, default=5.0)
    In_state = serializers.BooleanField(default=False)
    
    #method to get the job data based on the Job_ID passed in. Share the serialized data
    def get_job_object(self, obj):
        try:
            job_id = obj['Job_ID']
            print(f"get_job_object - Retreivng job ID={job_id}")
            job_data = Job.objects.get(id=job_id)
        #print(JobSerializer(job_data).data)
            return JobSerializer(job_data).data
        except Job.DoesNotExist:
            print(f"Error in Calculate Serializer Job ID {job_id} not exist in database")
            raise serializers.ValidationError({'Error in get_job_object': f'Job ID {job_id} not exist in database'})
        except Exception as e:
            print(f"Unexpexted Error: {str(e)}")
            raise serializers.ValidationError({'Error in get_job_object': str(e)})
    #method to get the university data based on the University_ID passed in. Share the serialized data
    def get_unv_object(self, obj):
        try:
            unv_id = obj['University_ID']
            print(f"get_unv_object - Retreivng University ID={unv_id}")
            unv_data = University.objects.get(id=unv_id)
            return UniversitySerializer(unv_data).data
        except University.DoesNotExist:
            print(f'Error in gett_unv_object - University ID {unv_id} not exist in database')
            raise serializers.ValidationError({'Error in get_unv_object': f'University ID {unv_id} not exist in database'})
        except Exception as e:
            print(f"Unexpexted Error: {str(e)}")
            raise serializers.ValidationError({'Error in get_job_object': str(e)})
    #method to get the loan total after graduation. 
    #Raise validation error is budget is greater than tuition
    def get_loan_total(self, obj):
        try:
            print("get_loan_total - Getting loan total after college")
            unv_id = obj['University_ID']
            unv_data = University.objects.get(id=unv_id)
            yearly_budget = obj['Budget']
            years = obj['Years']
            #checking if In_state is true. If it is get the in state tuition of the university
            if(obj['In_state']):
                if(yearly_budget > unv_data.in_state):
                    print(f"Error get_loan_total: Amount ${yearly_budget} is greating than {unv_data.name} in state tuition of ${unv_data.in_state}. You will have NO Loans after school")
                    raise serializers.ValidationError({'Budget Error': f'Amount ${yearly_budget} is greating than {unv_data.name} in state tuition of ${unv_data.in_state}. You will have NO Loans after school'})
                return (unv_data.in_state - yearly_budget) * years
            if(yearly_budget > unv_data.out_state):
                    print(f"Error get_loan_total: Amount ${yearly_budget} is greating than {unv_data.name} in state tuition of ${unv_data.in_state}. You will have NO Loans after school")
                    raise serializers.ValidationError({'Budget Error': f'Amount ${yearly_budget} is greating than {unv_data.name} out state tuition of ${unv_data.out_state}. You will have NO Loans after school'})
            return (unv_data.out_state - yearly_budget) * years
        except University.DoesNotExist:
            print(f'Error in Calculate Seriliazer University ID {unv_id} not exist in database')
            raise serializers.ValidationError({'Error in get_loan_total': f'University ID {unv_id} not exist in database'})
        except Exception as e:
            print(f"Unexpexted Error: {str(e)}")
            raise serializers.ValidationError({'Error in get_loan_total': str(e)})

