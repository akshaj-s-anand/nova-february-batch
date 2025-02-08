from django.shortcuts import render
from django.contrib.auth.models import User, Group
from complaint.models import Complaint
# Create your views here.
def dashboard(request):
    user = User.objects.all()
    customers = User.objects.filter(groups__id=1)
    users_count = User.objects.count()  
    customers_count = User.objects.filter(groups__id=1).count() 
    complaints = Complaint.objects.all()
    complaint_count = Complaint.objects.count()

    
    context = {
        'users': user,
        'customers':customers,
        'users_count': users_count,
        'customers_count': customers_count,
        'complaint_count': complaint_count,
        'complaints': complaints,
    }
    
    return render(request, 'dashboard/index.html', context)
