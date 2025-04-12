from django.contrib import admin
from .models import Item, Claim

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'location', 'date_reported', 'reported_by')
    list_filter = ('status', 'category', 'date_reported')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date_reported'
    list_per_page = 20

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('item', 'claimant', 'status', 'date_claimed')
    list_filter = ('status', 'date_claimed')
    search_fields = ('item__title', 'claimant__username', 'description')
    date_hierarchy = 'date_claimed'
    list_per_page = 20
