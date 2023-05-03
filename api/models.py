import datetime

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

# for auto delete

from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from celery import shared_task




class Register(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    picture = models.ImageField(upload_to='picture', null=True, blank=True)
    phone = PhoneNumberField(max_length=13, null=True, blank=True)
    profession = models.CharField(max_length=30, blank=True, null=True)


    def __str__(self):
        return self.name




class Found(models.Model):
    item_id = models.BigAutoField(primary_key=True, auto_created=True)
    image = models.ImageField(upload_to='img_found', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=256, null=True, blank=True)
    place_found = models.CharField(max_length=256, null=True, blank=True)
    date_found = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    mention = models.CharField(max_length=256, null=True, blank=True)
    isFound = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-updated']

class Job(models.Model):
    job_id = models.BigAutoField(primary_key=True, auto_created=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=216, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    number_needed = models.CharField(max_length=16)
    location = models.CharField(max_length=256,  null=True, blank=True)
    payment = models.CharField(max_length=216,  null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField( auto_now_add=True,)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated']

@receiver(post_save, sender=Job)
def scheduler(sender, instance, **kwargs):
    deletion_time = instance.date_created + timedelta(hours=24)
    delete_instance.apply_async(args=[instance.job_id], eta=deletion_time)


@shared_task
def delete_instance(instance_job_id):
    # Retrieve the instance
    instance = Job.objects.get(id=instance_job_id)
    # Delete the instance if it hasn't been deleted already
    if not instance.deleted_at:
        instance.delete()

class Report(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(max_length=256,  null=True, blank=True)
    reason = models.CharField(max_length=256,  null=True, blank=True)
    date_reported = models.DateTimeField(auto_now=True,  null=True, blank=True)

    def __str__(self):
        return self.account

class Message(models.Model):
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    reciever = models.ForeignKey(Found, default=1, on_delete=models.CASCADE)
    message = models.TextField( null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return f' message from {self.author} to {self.reciever.author}'