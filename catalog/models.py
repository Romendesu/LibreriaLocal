from django.db import models
from django.urls import reverse
from utils import LOAN_STATUS
from django.contrib.auth.models import User
import uuid

'''
Modelo para el género del libro
'''

class Genre(models.Model):
    # Campos del modelo
    name = models.CharField(
        max_length = 200,
        help_text= "Genero del libro (Ciencia ficción, Poesía, Sátira)"      
    )

    # Metodos del modelo
    def __str__(self) -> self:
        return self.name


'''

Modelo para el libro

'''
class Book(models.Model):
    # Campos del modelo
    title = models.CharField(
        max_length = 200
    )

    author = models.ForeignKey(
        'Author',                       # En caso de tener una clase, se asigna la clase
        on_delete = models.SET_NULL,
        null = True                     # Podemos establecer al Autor como nulo
    )

    summary = models.TextField(
        max_length = 1000,
        help_text = "Ingrese una breve descripcion del libro"
    )

    isbn = models.CharField(
        "ISBN",
        max_length = 13,
        help_text = '13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )

    genre = models.ManyToManyField(
        Genre,
        help_text="Ingrese un genero para el libro"
    )


    # Metodos del modelo
    def __str__(self) -> self:
        return self.title
    
    # Obtener ruta absoluta
    def get_absolute_url(self):
        return reverse('book-detail', args = [str(self.id)])

    # Mostrar el genero del libro
    def display_genre(self):
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

'''
Modelo para la instancia del libro
'''

class BookInstance(models.Model):
    # Campos del modelo
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        help_text="Un único ID por cada libro"
    )

    book = models.ForeignKey(
        'Book', 
        on_delete = models.SET_NULL,
        null = True
    )

    imprint = models.CharField(
        max_length = 200
    )

    due_back = models.DateField(
        null = True,
        blank = True
    )

    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = 'Disponibilidad del libro'
    )

    language = models.ForeignKey(
        "Language",
        on_delete = models.SET_NULL,
        null = True
    )

    borrower = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    # Metaclase para la instancia del libro
    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)
        
    # Representacion al invocar al modelo
    def __str__(self):
        return f'{self.id} - {self.book.title}'


'''

Modelo para el autor del libro

'''

class Author(models.Model):
    # Campos del modelo
    
    first_name = models.CharField(
        max_length = 100
    )

    last_name = models.CharField(
        max_length = 100
    )

    date_of_birth = models.DateField(
        null = True,
        blank = True
    )

    date_of_death = models.DateField(
        null = True,
        blank = True
    )

    # Obtener ruta absoluta
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    # Representacion del modelo
    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"



'''

Modelo para el lenguaje

'''

class Language(models.Model):
    name = models.CharField(
        max_length = 200,
        unique = True,
        help_text= "Ingrese un lenguaje (p.ej: Inglés, Francés, Español)"
    )

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


from datetime import date

@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False