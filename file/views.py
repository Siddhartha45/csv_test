from django.shortcuts import render
import csv
from .forms import UploadFileForm
from .models import Employee
import os
from django.conf import settings
from django.views.generic.edit import DeleteView, UpdateView
from django.db.models.functions import Concat
from django.db.models import Value
from django.core.paginator import Paginator


def employee_list(request):
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES['file']
            
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', file.name)
            with open(file_path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
                f.seek(0) 
                data = f.read().decode('utf-8').splitlines()
            
            reader = csv.DictReader(data)
            for row in reader:
                employee = Employee(
                    first_name = row['First Name'],
                    last_name = row['Last Name'],
                    dob = row['Date of Birth'],
                    salary = row['Salary']
                )
                employee.save()            
    else:
        form = UploadFileForm()
        
    employees = Employee.objects.all()
    sort_column = request.GET.get("sort_by", None)
    if sort_column:
        employees = employees.order_by(sort_column)
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'form': form, 'employees': employees, 'page_obj': page_obj, 'num_pages': paginator.num_pages, 'sort_column': sort_column}
    return render(request, 'file/employee.html', context) 


class DeleteEmployee(DeleteView):
    model = Employee
    template_name = 'file/delete_employee.html'
    success_url = '/'
    
    
class EditEmployee(UpdateView):
    model = Employee
    template_name = 'file/edit_employee.html'
    fields = ['first_name', 'last_name', 'dob', 'salary']
    success_url = '/'
    
    
def search_employee(request):
    search_term = request.GET.get('search', '')
    employees = Employee.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).filter(full_name__icontains=search_term)
    return render(request, 'file/search_employee.html', {'employees': employees, 'search_term': search_term})
