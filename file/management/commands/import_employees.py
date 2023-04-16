import csv
from django.core.management.base import BaseCommand
from file.models import Employee


class Command(BaseCommand):
    help = 'Import employees from a CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        
    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                employee = Employee(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    dob=row['Date of Birth'],
                    salary=row['Salary']
                )
                employee.save()
        self.stdout.write(self.style.SUCCESS('Employees imported successfully.'))