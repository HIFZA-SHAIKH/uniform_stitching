from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm, StudentMeasurementForm, FabricAccessoryForm, OrderForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, StudentMeasurement, FabricAccessory, Order
from django.db.models import Count

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'stitching/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'stitching/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def add_measurement(request):
    if request.method == 'POST':
        form = StudentMeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentMeasurementForm()
    return render(request, 'stitching/add_measurement.html', {'form': form})


def add_fabric(request):
    if request.method == "POST":
        form = FabricAccessoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fabric_list')  # Redirect to fabric list after saving
    else:
        form = FabricAccessoryForm()

    return render(request, 'stitching/add_fabric.html', {'form': form})

def fabric_list(request):
    fabrics = FabricAccessory.objects.all()
    return render(request, 'stitching/fabric_list.html', {'fabrics': fabrics})


@login_required
@login_required
def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()  # Directly save since student name comes from measurement
            return redirect("order_list")
    else:
        form = OrderForm()

    return render(request, "stitching/create_order.html", {"form": form})

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'stitching/order_list.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST.get('status')
        order.save()
        return redirect('order_list')

    return render(request, 'stitching/update_order.html', {'order': order})

@login_required
def dashboard(request):
    # User Statistics
    total_users = CustomUser.objects.count()
    role_counts = CustomUser.objects.values('role').annotate(count=Count('role'))

    # Student Measurements
    total_measurements = StudentMeasurement.objects.count()
    recent_measurements = StudentMeasurement.objects.order_by('-id')[:5]  # Show last 5 entries

    # Fabric & Accessories
    total_fabrics = FabricAccessory.objects.count()
    low_stock_fabrics = FabricAccessory.objects.filter(quantity__lt=5)  # Alert for low stock
    fabric_summary = FabricAccessory.objects.values('name', 'quantity', 'unit_price')

    # Orders Overview
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    recent_orders = Order.objects.order_by('-order_date')[:5]  # Show last 5 orders

    context = {
        'total_users': total_users,
        'role_counts': role_counts,
        'total_measurements': total_measurements,
        'recent_measurements': recent_measurements,
        'total_fabrics': total_fabrics,
        'low_stock_fabrics': low_stock_fabrics,
        'fabric_summary': fabric_summary,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
    }

    return render(request, 'stitching/dashboard.html', context)

def measurement_list(request):
    measurements = StudentMeasurement.objects.all()
    return render(request, 'stitching/measurement_list.html', {'measurements': measurements})