from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Регистрация простых моделей, для которых не нужны кастомные колонки
admin.site.register(Genre)
admin.site.register(Language)


# Настройка отображения Авторов в админке
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Исправили опечатку: 'date_of_birth' вместо 'data_of_birth'
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Author, AuthorAdmin)


# Настройка вывода экземпляров книг прямо внутри страницы самой книги (Inline)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# Настройка отображения Книг в админке
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

    # Вернули метод отображения жанров, чтобы админка не падала
    def display_genre(self, obj):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in obj.genre.all()[:3]])
        
    display_genre.short_description = 'Genre'


# Настройка отображения Конкретных экземпляров книг (BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )