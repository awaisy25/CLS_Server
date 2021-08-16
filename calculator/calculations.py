import math

#function to return the accrued interest of loan after 30 days
def interest_accrued(current_loan_total, interest_rate):
    daily_interest_rate = interest_rate / 360 #360 days since 30 days periods for 12 months
    interest_charge = round(((current_loan_total * daily_interest_rate) * 30),2)
    return interest_charge

#function to return minimum income percentage required. If greater than 100 inform career won't be able to pay off loans
def get_min_income_percentage(salary, loan_total, interest):
    interest_rate = interest_accrued(loan_total, interest)
    monthly_salary = salary / 12
    income_percentage = (interest_rate / monthly_salary) * 100#math is montly_salary * min_percentage = interest_rate, min_percentage is the value wanted
    #need to mutiply by 100 since default view is shown in hundreds
    income_percentage = round((income_percentage + 3),2) #adding 3 percent more so this way the duration isn't too long
    print(f"income_percentage: {income_percentage}")
    if(income_percentage > 100):
        return "Interest rate is greater than selected Career Salary"
    #return round((income_percentage + 3),2)#adding 3 percent more so this way the duration isn't too long
    return "Please increase Amount from Salary to at least {}%".format(income_percentage)

#conditonal to see if the monthly payment is less than the interest rate
def check_initial_payment(salary, loan_total, interest, per_income):
    payment = (salary / 12) * per_income
    logger.info(f"From check_initial payment function payment is: {payment}")
    interest_rate = interest_accrued(loan_total, interest)
    print(f"Check initial payment came out as {interest_rate > payment}")
    return (interest_rate > payment)

    
#recursion method to pay off the loans based on the inputs, return the num of months
def payoff_calc(salary,loan_total,interest,per_income):
    logger.info("Pay off calculations start")
    months = 0 #month will be incremented
    amount_paid = loan_total # intial total
    interest_paid = 0 
    logger.info("Pay off calcultions initial values loan total " + str(loan_total))
    while(loan_total > 0):
        #check how many years it has been to determin the salary. 0-3 years entry, 3-8 years middle, 8+ years senior
        if(months < 36):
            monthly_sal = round(((salary.entry / 12) * per_income), 2)
        elif(months < 96):
            monthly_sal = round(((salary.middle / 12) * per_income), 2)
        else:
            monthly_sal = round(((salary.senior / 12) * per_income), 2)
        #have a variable to return how much you have payed towards interests
        interest_charge = interest_accrued(loan_total, interest)
        interest_paid = interest_paid + interest_charge
        #adding interest charge first then putting in monthly payment
        loan_total = loan_total + interest_charge
        loan_total = loan_total - (monthly_sal)
        months +=1
    #subtract a month if the last total loan amount was one dollar or less. extra month unecessary
    months = months - 1 if math.ceil(monthly_sal) == math.ceil(abs(loan_total)) else months
    #have a variable to show total paid in loans + interest
    amount_paid = amount_paid + interest_paid
    results = {"Time": months, "Total_paid": round(amount_paid), "Interest_paid": round(interest_paid)}
    return results