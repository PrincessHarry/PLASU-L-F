from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Item, Claim, Notification

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'full_name',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

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

admin.site.register(Notification)
