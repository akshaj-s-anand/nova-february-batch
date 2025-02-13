from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from complaint.models import Item, SubItem, ComplaintStatuses
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ItemForm,ComplaintStatusForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('sample')
        
            else:
                messages.error(request, f"Sorry {username}, you do not have permission to access this page.")
        else:
            messages.error(request, 'Invalid username or password')    
            
        
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def permission_denied(request):
    return render(request, 'home/permission_error.html')


@login_required
def viewwitem(request):
    if not request.user.is_superuser:
        return redirect(reverse_lazy('permission_denied')) 
    
    items = Item.objects.all()  # Get items

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
        data = list(items.values('id', 'item_name'))
        return JsonResponse(data, safe=False)  

    # Normal request → Render HTML with preloaded items
    return render(request, 'home/view_item.html')


@login_required
def add_or_update_item(request, pk=None):
    if not request.user.is_superuser:
        return redirect(reverse_lazy('permission_denied')) 
    
    if pk:  # If pk is provided, fetch the existing item (Update mode)
        item = get_object_or_404(Item, id=pk)
    else:  # If no pk, create a new item (Add mode)
        item = None

    if request.method == "POST":
        if 'delete' in request.POST:  # If 'delete' button is pressed
            item.delete()
            return redirect(reverse_lazy('view_item'))  # Redirect after deletion

        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('view_item'))  # Redirect to item list

    else:
        form = ItemForm(instance=item)

    return render(request, 'home/add_item.html', {'form': form, 'item': item})


@login_required
def view_complaint_statuses(request):
    if not request.user.is_superuser:
        return redirect(reverse_lazy('permission_denied')) 
    
    statuses = ComplaintStatuses.objects.all()
    return render(request, 'home/view_complaint_statuses.html', {'statuses': statuses})

@login_required
def add_or_update_complaint_status(request, pk=None):
    if not request.user.is_superuser:
        return redirect(reverse_lazy('permission_denied')) 
    
    if pk:  # Update mode
        status = get_object_or_404(ComplaintStatuses, id=pk)
    else:  # Add mode
        status = None

    if request.method == "POST":
        if 'delete' in request.POST:  # Handle deletion
            status.delete()
            return redirect(reverse_lazy('view_complaint_statuses'))  

        form = ComplaintStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('view_complaint_statuses'))  

    else:
        form = ComplaintStatusForm(instance=status)

    return render(request, 'home/add_complaint_status.html', {'form': form, 'status': status})