from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
from django.apps import apps
import calendar
# Create your views here.
from .models import Employee
from customers.models import Customer

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the employee model from the other app, it can now be used to query the db for Employees
    Employee = apps.get_model('employees.Employee')
    return render(request, 'employees/employee_index.html')

@login_required
def employee_index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    
    try:
        # This line will return the employee record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        employee_zip_code = logged_in_employee.zip_code
        my_date = date.today()
        weekday = calendar.day_name[my_date.weekday()]
        local_customers = Customer.objects.filter(zip_code = employee_zip_code)
        my_weekly_pickups = Customer.objects.filter(weekly_pickup = weekday)
        my_one_time_pickups = Customer.objects.filter(one_time_pickup = my_date)
        

       
        
        context = {
            'logged_in_employee': logged_in_employee,
            'my_date': my_date,
            'weekday': weekday,
            'local_customers': local_customers,
            'my_weekly_pickups': my_weekly_pickups,
            'my_one_time_pickups': my_one_time_pickups
        }
        return render(request, 'employees/employee_index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create_employee'))


@login_required
def create_employee(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:employee_index'))
    else:
        return render(request, 'employees/create_employee.html')

@login_required
def edit_employee_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:employee_index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_employee_profile.html', context)

        
def register_pickup(request):
    # Page to select pickups to complete
    logged_in_user = request.user
    Customer = apps.get_model('customers', 'Customer')
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    employee_zip_code = logged_in_employee.zip_code
    local_customers = Customer.objects.filter(zip_code = employee_zip_code)

    # Get the current user and the associated employee object
    current_user = request.user
    current_employee = Employee.objects.get(user = current_user)

   
    if request.method == "POST":
        
        today = datetime.date.today()

        
        for customer_id in selected_customer_ids:
            current_customer = Customer.objects.get(id=customer_id)
            current_pickup = CompletedPickup(date=today, customer=current_customer, employee=current_employee)
            current_pickup.save()
           
            charge_customer(current_customer)

        return HttpResponseRedirect(reverse("employees:employee_index"))
    else:
        context = {
            "user" : current_user,
            
        }
        return render(request, 'employees/confirmed_pickups.html', context)