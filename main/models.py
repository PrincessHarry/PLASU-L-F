from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Item(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('claimed', 'Claimed'),
    ]
    
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('documents', 'Documents'),
        ('accessories', 'Accessories'),
        ('books', 'Books'),
        ('others', 'Others'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    location = models.CharField(max_length=200)
    date_reported = models.DateTimeField(default=timezone.now)
    date_occurred = models.DateTimeField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_items')
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_items')
    is_active = models.BooleanField(default=True)
    contact_info = models.CharField(max_length=200)
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    class Meta:
        ordering = ['-date_reported']

class Claim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    date_claimed = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField()
    proof_of_ownership = models.TextField()
    admin_notes = models.TextField(blank=True, null=True)
    resolved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Claim for {self.item.title} by {self.claimant.username}"

    class Meta:
        ordering = ['-date_claimed']

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('claim_submitted', 'Claim Submitted'),
        ('claim_approved', 'Claim Approved'),
        ('claim_rejected', 'Claim Rejected'),
        ('item_claimed', 'Item Claimed'),
        ('new_claim', 'New Claim'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.recipient.username}"
