from django.contrib import admin
from complaint.models import Complaint, SubItem, Item
# Register your models here.

admin.site.register(Complaint)
admin.site.register(SubItem)
admin.site.register(Item)