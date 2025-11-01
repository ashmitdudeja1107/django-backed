from django.contrib import admin
from .models import Task, Note

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'completed', 'created_at', 'due_date']
    list_filter = ['status', 'completed', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'task', 'created_at', 'file']
    list_filter = ['created_at', 'task']
    search_fields = ['title', 'content', 'user__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']