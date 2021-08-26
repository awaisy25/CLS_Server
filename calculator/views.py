from django.http.response import HttpResponse
from .serializers import JobSerializer, UniversitySerializer, SalarySerializer, CalculateSerializer
from .models import Job, University, Salary
from rest_framework.views import APIView
from rest_framework.response import Response
from . import calculations
#Setting up logging

#Function view to display friendly message when first getting on the initial Route
def Intro(request):
    return HttpResponse("Hello From Calculate Student Loans")
class Jobs(APIView):
    def get(self, request, format=None):
        try:
            print("GET Request - Retrieving all Jobs")
            Jobs = Job.objects.all()
            serializer = JobSerializer(Jobs, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            #these errors client doesn't need a response
            return Response({"Error": f"Unexpected Error: {str(e)}"}, status=404)


#retrieving all university
class Universities(APIView):
    def get(self, request, format=None):
        try:
            print("GET Request - Retrieving all Universities")
            Universities = University.objects.all()
            serializer = UniversitySerializer(Universities, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return Response({"Error": f"Unexpected Error: {str(e)}"}, status=404)
#retrieving university based by id
class UniversityById(APIView):
    def get(self, request, pk, format=None):
        try:
            print(f"GET Request - Retrieiving University with ID {pk}")
            university = University.objects.get(pk=pk)
            serializer = UniversitySerializer(university)
            print(f"GET: Sending University {serializer.data}")
            return Response(serializer.data)
        except:
            print(f'Error 404: University does not have ID {pk}')
            return Response({'Error': f'University does not have ID {pk}'}, status=404)

#view to retrive both the jobs and universities. url param will be jandu
class JandU(APIView):
    def get(self, request, format=None):
        try:
            Jobs = Job.objects.all()
            Universities = University.objects.all()
            unv_serializer = UniversitySerializer(Universities, many=True)
            job_serializer = JobSerializer(Jobs, many=True)
            #have both serilizers in dictionary so its easy to filter in client side
            result_data = {"Jobs": job_serializer.data, "Universities": unv_serializer.data}
            print(f'GET: Sending both Jobs and Universities')
            return Response(result_data)
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            #these errors don't need to return a message to the client
            return Response({"Error": f"Unexpected Error: {str(e)}"}, status=404)
class Salaries(APIView):
    def post(self, request, format=None):
        #function get salary data
        try:
            post_data = request.data
            #since not using seriliaizer validator, creating field validation similar to serilaizer field validation
            if 'Job_ID' not in post_data:
                print(f"Error 400: Job_ID field missing")
                return Response({"Error": {"Job_ID": ["This field is required."]}}, status=404)
            job_id = post_data['Job_ID']
            #if state field not in or is null return US average
            if 'State' not in post_data or post_data['State'] == '' or post_data['State'] == None:
                print("State is set to US")
                state = "US" #if No State field or empty field retrieve the US average for the job
            else:
                state = post_data['State'].upper() #all states in database are in upper case
            salary = Salary.objects.get(job=job_id, state=state)
            serializer = SalarySerializer(salary)
            print(f"POST: Sending Salary data {serializer.data}")
            return Response(serializer.data)
        except Salary.DoesNotExist:
            print(f"Error: Job not found within {state}")
            return Response({"Status": 400, "Message":  f"Job not found within state {state}"})
        except Exception as e:
            print(f"Error: {str(e)}")
            #these errors don't send a response to the client
            return Response({"Error": str(e)}, status=404)

#this is the method that will have the calculation logic and functionality
class PayOffEstimate(APIView):
    #getting all of the fields from the form data
    def post(self, request, format=None):
        try:
            #print(request.data)
            serializer = CalculateSerializer(data=request.data)
        except Exception as e:
            print("Error 400: Something went wrong in Serializer")
            return Response({"Error": str(e)}, status=404)
        if serializer.is_valid():
            print("POST: Creating and returning calculations")
            #since serializer data is immutable have to append to empty dictionary in order to add other data to the result
            result_data = {}
            #print(serializer.data)
            result_data.update(serializer.data)
            #retriving the salary based on job and state. 
            if serializer.data['State'] == '' or serializer.data['State'] == None:
                print("State is set to US")
                state = "US" #if No State field or empty field retrieve the US average for the job
                result_data['State'] = 'US'
            else: 
                #States in database are all uppercase have to use .upper if there is a string value
                state = serializer.data['State'].upper()
            try:
                salary = Salary.objects.get(job=serializer.data['Job_ID'], state=state)
                print(f"Salary object {str(salary)}")
            #exception for when Salary object does not exist
            except Salary.DoesNotExist:
                print(F"Error: Job {serializer.data['Job']['title']} not found within State {serializer.data['State']}")
                return Response({"Status": 400, "Message": f"Job {serializer.data['Job']['title']} not found within State {serializer.data['State']}"})
            #last validation to see if interest rate is greater than the first month payment
            if(calculations.check_initial_payment(salary=salary.entry, loan_total=result_data['Loan_total'], interest=(result_data['Interest_rate'] / 100), per_income=(result_data['Percent_income'] / 100)) == True):
                min_percentage_response = calculations.get_min_income_percentage(salary=salary.entry, loan_total=result_data['Loan_total'], interest=(result_data['Interest_rate'] / 100))
                print(f"Error: Amount from Salary not enough to cover Interest Rate {min_percentage_response}")
                return Response({"Status": 400, "Message": f"Amount from Salary not enough to cover Interest Rate {min_percentage_response}"})
            #appending salary data to result dictionary
            Salary_data = {'Salary': {'entry': salary.entry, 'middle': salary.middle, 'senior': salary.senior}}
            result_data.update(Salary_data)
            #getting the estimates. Payoff time, total paid towards interests, total amount to payoff loans
            estimates = calculations.payoff_calc(salary=salary, loan_total=result_data['Loan_total'], interest=(result_data['Interest_rate'] / 100), per_income=(result_data['Percent_income'] / 100))
            result_data.update(estimates)
            #removing Job_ID and university from dictionary since its shown in the object
            result_data.pop('Job_ID')
            result_data.pop('University_ID')
            print(f"Data to send {str(result_data)}")
            return Response(result_data)
        else:
            print(f"Unexpected error {serializer.errors}")
            return Response({"Status": 400, "Message": serializer.errors})


        


