from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import User, Donation, Verification, Message, BusinessProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# List all users (e.g., donors, recipients, etc.)
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

# View user details
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

# Create new user
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'password_hash', 'communication_method']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

# Update existing user
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'communication_method']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

# List all donations
@login_required
def donation_list(request):
    donations = Donation.objects.all()
    return render(request, 'donations/donation_list.html', {'donations': donations})

# View a specific donation
@login_required
def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, 'donations/donation_detail.html', {'donation': donation})

# Create a new donation
@login_required
def donation_create(request):
    if request.method == 'POST':
        # Handle form submission and save the donation
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donation-list')
    else:
        form = DonationForm()
    return render(request, 'donations/donation_form.html', {'form': form})

# Verify a donation
@login_required
def donation_verify(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    # Assume verification logic is here
    verification = Verification.objects.create(donation=donation, verified_by=request.user, verification_status='verified')
    return redirect('donation-detail', pk=pk)

@login_required
def message_list(request):
    messages_sent = Message.objects.filter(sender=request.user)
    messages_received = Message.objects.filter(recipient=request.user)
    return render(request, 'messages/message_list.html', {'messages_sent': messages_sent, 'messages_received': messages_received})

# Send a new message
@login_required
def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message-list')
    else:
        form = MessageForm()
    return render(request, 'messages/message_form.html', {'form': form})

class VerificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Verification
    fields = ['verification_status', 'verification_notes']
    template_name = 'verifications/verification_form.html'
    success_url = reverse_lazy('donation-list')

class BusinessProfileListView(LoginRequiredMixin, ListView):
    model = BusinessProfile
    template_name = 'business_profile/business_profile_list.html'
    context_object_name = 'business_profiles'

# View a single business profile
class BusinessProfileDetailView(LoginRequiredMixin, DetailView):
    model = BusinessProfile
    template_name = 'business_profile/business_profile_detail.html'
    context_object_name = 'business_profile'

# Create a new business profile
class BusinessProfileCreateView(LoginRequiredMixin, CreateView):
    model = BusinessProfile
    fields = ['business_name', 'description', 'registration_number']
    template_name = 'business_profile/business_profile_form.html'
    success_url = reverse_lazy('business-profile-list')

# Update an existing business profile
class BusinessProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = BusinessProfile
    fields = ['business_name', 'description', 'registration_number']
    template_name = 'business_profile/business_profile_form.html'
    success_url = reverse_lazy('business-profile-list')

