from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language
# Establecer modelos inline
class BookInstanceInline(admin.TabularInline):
    model = BookInstance

# Registrar modelos empleando genéricos
@admin.register(Book)
class BookAdmin(admin.ModelAdmin): 
    list_display = ("title", "author", "display_genre")
    inlines = [BookInstanceInline]
    
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin): 
    # Aplicar un cuadro de filtro
    list_filter = ('status', 'due_back')

    # Informar el estado de un libro
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint','language', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

@admin.register(Author)
class AuthorInstance(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]        # Re-Organizar los campos


# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)