from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class ComplaintStatuses(models.Model):
    id= models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.status
    

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.item_name
        
class SubItem(models.Model):
    id = models.AutoField(primary_key=True)
    sub_item_name = models.CharField(max_length=20)
    item = models.ForeignKey(Item, related_name='sub_items', on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_item_name


class Components(models.Model):
    id = models.AutoField(primary_key=True)
    component = models.CharField(max_length=20)
    
    def __str__(self):
        return self.component

class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_complaints')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    
    CUSTOMER_TYPE_CHOICES = (
        ('person', 'person'),
        ('company', 'company'),
    )
    
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES, null=True, blank=True)
    
    PICK_POINT_CHOICES = (
        ('onsite', 'onsite'),
        ('offsite', 'offsite'),
    )
    
    pick_point = models.CharField(max_length=10, choices=PICK_POINT_CHOICES, null=True, blank=True)
    
    appoinment_date = models.DateTimeField()
    complaint_description = models.TextField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assigned_complaints')
    status = models.ForeignKey(ComplaintStatuses, on_delete=models.CASCADE, null=True, blank=True)
    technical_report = models.TextField(null=True, blank=True)
    components_used = models.ManyToManyField(Components)
    bill_amount = models.IntegerField(default=0)
    

    def __str__(self):
       return f"Complaint ID: {self.id} by {self.customer.username}"

    
class ComplaintUser(models.Model):
    id = models.AutoField(primary_key=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"ComplaintUser for {self.complaint} and {self.user}"


# Signal to automatically create a ComplaintUser when a Complaint is created
@receiver(post_save, sender=Complaint)
def create_complaint_user(sender, instance, created, **kwargs):
    if created:  # Only run if a new Complaint instance is created
        ComplaintUser.objects.create(complaint=instance, user=instance.customer)
        
        
