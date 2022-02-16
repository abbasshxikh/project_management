from django.db import models
from accounts.models import User, TechnologyStack
from accounts.constants import StatusConstants
from file_storage.models import FileStorage
from django.contrib.contenttypes.fields import GenericRelation


class Project(models.Model):
    title = models.CharField(max_length=80)
    user = models.ManyToManyField(User, through="UserProject")
    status = models.CharField(max_length=7, choices=StatusConstants.get_choices(), default=StatusConstants.CREATED.value)
    project_start_date = models.DateField(null=True, blank=True)
    project_end_date = models.DateField(null=True, blank=True)
    technology_stack = models.ManyToManyField(TechnologyStack, related_name="project_technology")
    description = models.TextField(null=True, blank=True)

    files = GenericRelation(FileStorage, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return (self.title) 


class ProjectRole(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return (self.name) 


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)
    user_active_date = models.DateField(null=True, blank=True)
    user_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return (self.role) 


class Topic(models.Model):
    topic_name = models.CharField(max_length=100, null=True, blank=True)
    technology_stack = models.ForeignKey(TechnologyStack, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.topic_name


class ReferenceLinks(models.Model):
    links = models.URLField(null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return (self.links)
