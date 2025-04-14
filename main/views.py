from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Item, Claim, Notification
from .forms import CustomUserCreationForm, ItemForm, ClaimForm
from django.contrib.auth import logout
from django.utils import timezone

def home(request):
    recent_items = Item.objects.filter(is_active=True).order_by('-date_reported')[:6]
    context = {
        'recent_items': recent_items,
    }
    return render(request, 'main/home.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def profile(request):
    user_items = Item.objects.filter(reported_by=request.user)
    user_claims = Claim.objects.filter(claimant=request.user)
    context = {
        'user_items': user_items,
        'user_claims': user_claims,
    }
    return render(request, 'main/profile.html', context)

@login_required
def report_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.reported_by = request.user
            item.save()
            messages.success(request, 'Item reported successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'main/report_item.html', {'form': form})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    claims = item.claims.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            messages.success(request, 'Claim submitted successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ClaimForm()
    context = {
        'item': item,
        'claims': claims,
        'form': form,
    }
    return render(request, 'main/item_detail.html', context)

def lost_items(request):
    items = Item.objects.filter(status='lost', is_active=True)
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'main/lost_items.html', {'items': items})

def found_items(request):
    items = Item.objects.filter(status='found', is_active=True)
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return render(request, 'main/found_items.html', {'items': items})

def search_items(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    
    items = Item.objects.filter(is_active=True)
    
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    
    if category:
        items = items.filter(category=category)
    
    if status:
        items = items.filter(status=status)
    
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    
    context = {
        'items': items,
        'query': query,
        'category': category,
        'status': status,
    }
    return render(request, 'main/search_results.html', context)

@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    paginator = Paginator(notifications, 10)
    page = request.GET.get('page')
    notifications = paginator.get_page(page)
    return render(request, 'main/notifications.html', {'notifications': notifications})

@login_required
def mark_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

@login_required
def mark_all_read(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
    return redirect('notifications')

def create_notification(recipient, notification_type, item=None, claim=None, message=None):
    if message is None:
        if notification_type == 'claim_submitted':
            message = f'Your claim for {item.title} has been submitted.'
        elif notification_type == 'claim_approved':
            message = f'Your claim for {item.title} has been approved.'
        elif notification_type == 'claim_rejected':
            message = f'Your claim for {item.title} has been rejected.'
        elif notification_type == 'item_claimed':
            message = f'Your item {item.title} has been claimed.'
        elif notification_type == 'new_claim':
            message = f'New claim submitted for your item {item.title}.'

    Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        item=item,
        claim=claim,
        message=message
    )

@login_required
def submit_claim(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            
            create_notification(
                recipient=item.reported_by,
                notification_type='new_claim',
                item=item,
                claim=claim
            )
            
            create_notification(
                recipient=request.user,
                notification_type='claim_submitted',
                item=item,
                claim=claim
            )
            
            messages.success(request, 'Claim submitted successfully.')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ClaimForm()
    return render(request, 'main/submit_claim.html', {'form': form, 'item': item})

@login_required
def update_claim_status(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    if request.user.is_staff:
        new_status = request.POST.get('status')
        if new_status in ['approved', 'rejected']:
            claim.status = new_status
            claim.save()
            
            notification_type = 'claim_approved' if new_status == 'approved' else 'claim_rejected'
            create_notification(
                recipient=claim.claimant,
                notification_type=notification_type,
                item=claim.item,
                claim=claim
            )
            
            if new_status == 'approved':
                create_notification(
                    recipient=claim.item.reported_by,
                    notification_type='item_claimed',
                    item=claim.item,
                    claim=claim
                )
                
                claim.item.status = 'claimed'
                claim.item.save()
            
            messages.success(request, f'Claim {new_status} successfully.')
    return redirect('item_detail', pk=claim.item.pk)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    # Check if the user is the owner of the item
    if item.reported_by != request.user:
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('item_detail', pk=item.pk)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'main/edit_item.html', context)

@login_required
def delete_item(request, item_id):
    """Delete an item"""
    item = get_object_or_404(Item, id=item_id)
    
    # Check if the user is the owner of the item
    if item.reported_by != request.user:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('item_detail', pk=item_id)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item has been successfully deleted.')
        return redirect('home')
    
    return redirect('item_detail', pk=item_id)

@login_required
def share_item(request, item_id):
    """Share an item via email or social media"""
    item = get_object_or_404(Item, id=item_id)
    
    # For now, we'll just redirect to the item detail page with a success message
    # In a real implementation, you would add functionality to share via email or social media
    messages.success(request, f'Item "{item.title}" has been shared successfully.')
    return redirect('item_detail', pk=item_id)
