from django.db import models
from django.contrib.auth import get_user_model
from djangolar.abstract.models import BaseEntity
from django.core.validators import MaxValueValidator

User = get_user_model()

class Course(BaseEntity):
    title = models.CharField()
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='owned_courses', on_delete=models.CASCADE)


class Lesson(BaseEntity):
    title = models.CharField()
    content = models.TextField()
    order = models.DecimalField(max_digits=10, decimal_places=2)
    indentation = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5)])
    is_published = models.BooleanField(default=False)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)