from django.contrib import admin
from .models import Student, Book,Note

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'category')
    search_fields = ('title', 'author', 'description')
    readonly_fields = ('approval_token', 'created_at', 'updated_at')
    actions = ['approve_selected_books', 'reject_selected_books']

    def approve_selected_books(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected books have been approved.")
    approve_selected_books.short_description = "Approve selected books"

    def reject_selected_books(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected books have been rejected and deleted.")
    reject_selected_books.short_description = "Reject selected books"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'mail', 'created_at')
    search_fields = ('firstname', 'lastname', 'mail')
    
admin.site.register(Note)



# your_app/admin.py
"""
from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')
    search_fields = ('text',)
  """
