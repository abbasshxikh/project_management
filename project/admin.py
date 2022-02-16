from django.contrib import admin

# Register your models here.
from django.contrib import admin
from project.models import (
    Project,
    ProjectRole,
    UserProject,
    FileStorage,
    FileType,
    Topic,
    ReferenceLinks
   
)

admin.site.register(Project)
admin.site.register(ProjectRole)
admin.site.register(UserProject)
admin.site.register(FileStorage)
admin.site.register(FileType)
admin.site.register(Topic)
admin.site.register(ReferenceLinks)

