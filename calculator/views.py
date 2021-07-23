from django.http.response import HttpResponse
from django.shortcuts import render
from .serializers import JobSerializer, UniversitySerializer, SalarySerializer, CalculateSerializer
from .models import Job, University, Salary
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
# The HTTP Operations will only have Reads to the databases no Writes

class Jobs(APIView):
    def get(self, request, format=None):
        Jobs = Job.objects.all()
        serializer = JobSerializer(Jobs, many=True)
        return Response(serializer.data)
        
#retrieving all university
class Universities(APIView):
    def get(self, request, format=None):
        Universities = University.objects.all()
        serializer = UniversitySerializer(Universities, many=True)
        return Response(serializer.data)

#retrieving university based by id
class UniversityById(APIView):
    def get(self, request, pk, format=None):
        try:
            university = University.objects.get(pk=pk)
            serializer = UniversitySerializer(university)
            return Response(serializer.data)
        except:
            raise Http404

class Salaries(generics.ListAPIView):
    def post(self, request, format=None):
        #function get salary data
        try:
            post_data = request.data
            #since not using seriliaizer validator, creating field validation similar to serilaizer field validation
            if 'State' not in post_data:
                return Response({"Error": {"State": ["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)
            elif 'Job_ID' not in post_data:
                return Response({"Error": {"Job_ID": ["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)
            job_id = post_data['Job_ID']
            state = post_data['State']
            #if state is blank then return None when querying in Salary object
            if state == '':
                state = None
            else:
                state = state.upper() #all states in database are in upper case
            salary = Salary.objects.get(job=job_id, state=state)
            serializer = SalarySerializer(salary)
            return Response(serializer.data)
        except Salary.DoesNotExist:
            return Response({"Error": f"Job not found within state {state}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#this is the method that will have the calculation logic and functionality
class PayOffEstimate(APIView):
    #getting all of the fields from the form data
    def post(self, request, format=None):
        print(request.data)
        try:
            serializer = CalculateSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.data)
                return Response(serializer.data)
            else:
                return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        


