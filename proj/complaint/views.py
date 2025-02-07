from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from complaint.models import User, Group, Complaint
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def sample(request):
    
    user = User.objects.all()
    customers = User.objects.filter(groups__id=1)
    

    
    context = {
        'users': user,
        'customers':customers,
    }
    
    return render (request, 'complaints/sample.html', context)

def customer_complaints(request, user_id):
    # Get the user (User object) based on the user_id
    user = get_object_or_404(User, id=user_id)
    
    # Get complaints related to this user
    complaints = Complaint.objects.filter(customer=user)

    context = {
        'user': user,
        'complaints': complaints,
    }

    return render(request, 'complaints/customer_complaints.html', context)