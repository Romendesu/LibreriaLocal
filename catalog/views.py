from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

# Vista de inicio -> Retorna el HTML renderizado (el home)
def index(request):

    # Generar objetos principales
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Libros disponibles (STATUS = 'a')
    # NOTA: El filtro all() esta por defecto de forma implicita

    num_instances_avaiable = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    
    # Titulo de la pagina
    title = "Home"

    # Numero de visitas de la pagina
    num_visits = request.session.get("num_visits",0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # Convertir a parametro
    context = {
        'num_books':num_books, 
        'num_instances':num_instances,
        'num_instances_avaiable':num_instances_avaiable,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'title':title,
        'num_visits':num_visits,
    }
    # Renderizar el HTML con los datos de la variable de contexto
    return render(
        request,
        'index.html',
        context=context,
    )


# Vista de la lista de los libros
class BookListView(generic.ListView):
    # Llamamos al modelo de la base de datos
    model = Book
    # Empieza a paginar rutas GET a partir de 10 registros añadidos
    paginate_by = 10

    # Pasar variables de contexto
    def get_context_data(self, **kwargs):
        # Llamar a la implementacion para obtener contexto
        context = super(BookListView, self).get_context_data(**kwargs)

        # Obtener el blog del ID y agregarlo al contexto
        context["title"] = 'Vista de libros'

        # Devolver el contexto
        return context

    # Query que establece un filtro de los primeros 5 libros 
    queryset = Book.objects.filter()  

    # Especificar el nombre de la plantilla / ubicacion
    template_name = 'books/my_arbitrary_template_name_list.html'


# Vista del detalle de los libros
class BookDetailView(generic.DetailView):
    model = Book

# Vista del autor (la lista)
class AuthorListView(generic.ListView):
    model = Author
    # Paginamos los resultados en 10
    paginate_by = 10

    def get_context_data(self,**kwargs):
        # Sobreescribir el contexto
        context = super(AuthorListView, self).get_context_data(**kwargs)

        # Obtener el ID del blog y agregar al contexto
        context["title"] = 'Vista de autores'

        return context
    
    # Obtener todos los autores
    queryset = Author.objects.filter()

    # Especificar el nombre de la plantilla y su ubicación
    template_name = 'authors/author_list_template.html'

class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()                  # Obtienes el autor actual
        context['books'] = author.book_set.all()    # Todos los libros del autor
        return context


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')