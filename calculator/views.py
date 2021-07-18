from django.shortcuts import render
from .serializers import JobSerializer, UniversitySerializer
from .models import Job, University
from django.http import Http404
from rest_framework.views import APIView
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

