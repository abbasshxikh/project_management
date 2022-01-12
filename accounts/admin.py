from django.contrib import admin
from accounts.models import (
    User,
    Department,
    TechnologyStack,
    Designation,
    UserDetails,
    EmployeeTechnologyRating
)

admin.site.register(User)
admin.site.register(UserDetails)
admin.site.register(Department)
admin.site.register(TechnologyStack)
admin.site.register(Designation)
admin.site.register(EmployeeTechnologyRating)
