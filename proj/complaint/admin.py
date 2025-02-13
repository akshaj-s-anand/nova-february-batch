from django.contrib import admin
from complaint.models import Complaint, SubItem, Item, ComplaintStatuses, Components
# Register your models here.

admin.site.register(Complaint)
admin.site.register(SubItem)
admin.site.register(Item)
admin.site.register(ComplaintStatuses)
admin.site.register(Components)