from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
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
    logged_in_user = request.user
    if request.method == "POST":
        todays_date = date.today()
        get_id = request.POST.get('id')
        single_customer = Customer.objects.get(id=get_id)
        single_customer.date_of_last_pickup = todays_date
        single_customer.balance += 20
        single_customer.save()

        return HttpResponseRedirect(reverse('employees:employee_index'))
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        employee_zip_code = logged_in_employee.zip_code
        week_array = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        todays_date = date.today()
        day_of_week = week_array[todays_date.weekday()]
        customer_filter = Customer.objects.filter(zip_code=employee_zip_code)\
            .filter(weekly_pickup=day_of_week)\
            .exclude(date_of_last_pickup=todays_date)\
            .exclude(suspend_start=todays_date)\
            .exclude(suspend_end=todays_date)\
            .exclude(one_time_pickup=todays_date)

        one_time_filter = Customer.objects.filter(zip_code=employee_zip_code)\
            .filter(one_time_pickup=todays_date)\
            .exclude(date_of_last_pickup=todays_date)\

        context = {
            'logged_in_employee': logged_in_employee,
            'todays_date': todays_date,
            'day_of_week': day_of_week,
            'customer_filter': customer_filter,
            'one_time_filter': one_time_filter
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

def search_by_day(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    employee_zip_code = logged_in_employee.zip_code
    if request.method == "POST":
        get_weekday = request.POST.get('week')
        customer_filter = Customer.objects.filter(zip_code=employee_zip_code)\
            .filter(weekly_pickup=get_weekday)\

        chosen_week_day = get_weekday
        context = {
            'customer_filter': customer_filter,
            'logged_in_employee': logged_in_employee,
            'chosen_week_day': chosen_week_day
        }
        return render(request, 'employees/search_by_day.html', context)
    else:
        week_array = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        todays_date = date.today()
        todays_date_weekday = week_array[todays_date.weekday()]
        customer_filter = Customer.objects.filter(zip_code=employee_zip_code)\
            .filter(weekly_pickup=todays_date_weekday)
        chosen_week_day = todays_date_weekday
        context = {
            'customer_filter': customer_filter,
            'logged_in_employee': logged_in_employee,
            'chosen_week_day': chosen_week_day
        }
        return render(request, 'employees/search_by_day.html', context)
        