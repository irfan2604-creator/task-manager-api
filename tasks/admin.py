from django.contrib import admin
from .models import Task, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "category",
        "priority",
        "status",
        "due_date",
    )
    list_filter = ("priority", "status", "category")
    search_fields = ("title", "description", "owner__username", "category__name")
    ordering = ("-created_at",)
    list_editable = ("priority", "status", "category")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    list_per_page = 20
    list_select_related = ("owner", "category")
    
    fieldsets = (
    ("Task Information", {
        "fields": ("title", "description"),
    }),
    ("Task Settings", {
        "fields": ("priority", "status", "category", "owner", "due_date"),
    }),
    ("Timestamps", {
        "fields": ("created_at", "updated_at"),
    }),
)
        
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
