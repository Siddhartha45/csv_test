from django.urls import path
from . import views


urlpatterns = [
    path('', views.employee_list, name="employee"),
    path('employee/edit/<int:pk>', views.EditEmployee.as_view(), name='edit_employee'),
    path('delete/<int:pk>', views.DeleteEmployee.as_view(), name='delete_employee'),
    path('employee/search/', views.search_employee, name='search_employee'),
]
