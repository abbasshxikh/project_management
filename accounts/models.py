from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from accounts.constants import NonEmployeeConstants, RatingConstants


def validate_name(value):
    if TechnologyStack.objects.filter(name__iexact=value).exists():
        raise ValidationError("Technology already exists")
    return value
  
class Department(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Designation(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class TechnologyStack(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[validate_name])

    def __str__(self):
        return str(self.name)

class User(AbstractUser):
    """Custom user model that supports email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=255, null=True, blank=True)
    past_experience = models.FloatField(default=0, null=True, blank=True)
    verification = models.BooleanField(default=False)
    # files = GenericRelation("FileStorage", content_type_field='content_type', object_id_field='object_id')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.email)


class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joining_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    technology_stack = models.ManyToManyField(TechnologyStack, through="EmployeeTechnologyRating", related_name="employee_technology")
    
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    @classmethod
    def get(cls, id):
        return UserDetails.objects.get(id=id)
        
    def get_designation(self):
        return self.designation.name
    
    @property
    def is_employee(self):
        designation = self.get_designation()
        return not designation in NonEmployeeConstants.get_values()


class EmployeeTechnologyRating(models.Model):
    technology_stack = models.ForeignKey(TechnologyStack, on_delete=models.CASCADE)
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    rating = models.CharField(max_length=255, choices=RatingConstants.get_choices(), default=RatingConstants.AVERAGE.value)

    def __str__(self):
        return str(self.technology_stack) +  "/" + str(self.user) + "/" + str(self.rating)