from django.urls import path
from accounts.views import (
    ProjectView, 
)

app_name = 'projects'

urlpatterns = [
    path('create/', ProjectView.as_view(), name="project_creation"),
]