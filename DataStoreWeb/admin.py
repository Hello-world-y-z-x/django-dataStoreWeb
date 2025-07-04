from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import File, AccessLog

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'uploaded_by')

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'file')
    list_filter = ('action', 'timestamp', 'user')
    readonly_fields = ('timestamp',)
