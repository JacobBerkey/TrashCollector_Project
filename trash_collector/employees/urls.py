from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.employee_index, name="employee_index"),
    path('new/', views.create_employee, name="create_employee"),
    path('edit_employee_profile/', views.edit_employee_profile, name="edit_employee_profile"),
    path("<int:customers_id>/", views.update_weekly_pickups, name="update_weekly_pickups"),
    path("'<int:customers_id>/", views.update_one_time_pickups, name="update_one_time_pickups")
]

