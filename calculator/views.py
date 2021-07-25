from django.http.response import HttpResponse
from .serializers import JobSerializer, UniversitySerializer, SalarySerializer, CalculateSerializer
from .models import Job, University, Salary
from rest_framework.views import APIView
from rest_framework.response import Response
from . import calculations

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
            return Response({'Error': f'University does not have ID {pk}'}, status=status.HTTP_404_NOT_FOUND)

class Salaries(APIView):
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
        try:
            print(request.data)
            serializer = CalculateSerializer(data=request.data)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            #since serializer data is immutable have to append to empty dictionary in order to add other data to the result
            result_data = {}
            print(serializer.data)
            result_data.update(serializer.data)
            #retriving the salary based on job and state. 
            # States in database are all uppercase have to use .upper if there is a string value
            if serializer.data['State'] == '' or serializer.data['State'] == None:
                state = serializer.data['State']
            else: 
                state = serializer.data['State'].upper()
            try:
                salary = Salary.objects.get(job=serializer.data['Job_ID'], state=state)
            #exception for when Salary object does not exist
            except Salary.DoesNotExist:
                return Response({"Error": f"Job {serializer.data['Job']['title']} not found within State {serializer.data['State']}"}, status=status.HTTP_400_BAD_REQUEST)
            #last validation to see if interest rate is greater than the first month payment
            if(calculations.check_initial_payment(salary=salary.entry, loan_total=result_data['Loan_total'], interest=(result_data['Interest_rate'] / 100), per_income=(result_data['Percent_income'] / 100)) == True):
                min_percentage_response = calculations.get_min_income_percentage(salary=salary.entry, loan_total=result_data['Loan_total'], interest=(result_data['Interest_rate'] / 100))
                return Response({"Error": f"Amount from Salary not enough to cover Interest Rate {min_percentage_response}"}, status=status.HTTP_400_BAD_REQUEST)
            #appending salary data to result dictionary
            Salary_data = {'Salary': {'entry': salary.entry, 'middle': salary.middle, 'senior': salary.senior}}
            result_data.update(Salary_data)
            #getting the estimates. Payoff time, total paid towards interests, total amount to payoff loans
            estimates = calculations.payoff_calc(salary=salary, loan_total=result_data['Loan_total'], interest=(result_data['Interest_rate'] / 100), per_income=(result_data['Percent_income'] / 100))
            result_data.update(estimates)
            return Response(result_data)
        else:
            return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


        


