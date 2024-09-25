from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLE_CHOICES = (
    ('Candidate', 'Candidate'),
    ('HR', 'HR'),
)

class User(AbstractUser):
    # role = models.CharField(max_length=255, choices=ROLE_CHOICES, default=False)
    is_admin = models.BooleanField(default=False)
    is_masteruser = models.BooleanField(default=False)
    # is_hr= models.BooleanField('Is hr', default=False)
    # is_candidate = models.BooleanField('Is candidate', default=False)
    
class User_Details(models.Model):
    user_nm = models.ForeignKey(User, on_delete=models.CASCADE)
    res = models.FileField(upload_to='')
    job_role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.res}"
    
class Questions(models.Model):
    user_name = models.CharField(max_length=100)
    question_number = models.CharField(max_length=100)
    selected_answer = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user_name}"
    
class tech_test_model(models.Model):

    user_name = models.CharField(max_length=100)
    question_number = models.CharField(max_length=100)
    selected_answer = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user_name}"
    
class Contactus(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    msg = models.TextField()

    def __str__(self):
        return f"{self.name}"
    
class ForceSignoutUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user}"
    

class ForceSignout_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='')
    job_type = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user}"
    


JOB_CHOICES = (
    ('Python Developer', 'Python Developer'),
    ('Java Developer', 'Java Developer'),
    ('Data Scientist', 'Data Scientist'),
    ('AIML Engineer', 'AIML Engineer'),
    ('Backend Developer', 'Backend Developer'),
    ('.NET Developer', '.NET Developer'),
    ('Frontend Developer', 'Frontend Developer'),
    ('React Developer', 'React Developer'),
    ('Flutter Developer', 'Flutter Developer'),
    ('PHP Developer', 'PHP Developer'),
    ('Django Developer', 'Django Developer')

)

DEPARTMENT_CHOICES = (
    ('IT Department', 'IT Department'),
    ('HR Department', 'Human Resources Department'),
    ('Finance Department', 'Finance Department'),
)
class Job(models.Model):
    title = models.CharField(max_length=255, choices=JOB_CHOICES)
    department = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    def __str__(self):
        return f"{self.title}"
    


