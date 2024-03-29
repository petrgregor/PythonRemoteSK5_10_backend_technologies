from datetime import datetime
from logging import getLogger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView
from django_addanother.views import CreatePopupMixin
from django_addanother.widgets import AddAnotherWidgetWrapper

from viewer.models import *
from django.forms import Form, ModelChoiceField, Textarea, IntegerField, CharField, ModelMultipleChoiceField, \
    CheckboxSelectMultiple, ModelForm, DateField, SelectDateWidget, DateInput, SelectMultiple

LOGGER = getLogger()


# Create your views here.
def hello(request):
    return HttpResponse("Hello, World!")


def hello2(request, s):
    return HttpResponse(f"Hello, {s} world!")


def hello3(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Hello, {s} world!")


def hello4(request):
    return render(request, template_name='hello.html')


def hello5(request, s0):
    s1 = request.GET.get('s1', '')
    context = {'adjectives': [s0, s1, 'beautiful', 'wonderful']}
    return render(
        request,
        template_name='hello5.html',
        context=context
    )


def index(request):
    return render(request, 'index.html')


class GenreModelForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().capitalize()
        return name


class GenreCreateView(LoginRequiredMixin, CreateView):
    template_name = 'movie_create.html'  # TODO genre_create.html
    form_class = GenreModelForm
    success_url = reverse_lazy('index')


class GenreUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'genre_create.html'
    model = Genre
    form_class = GenreModelForm
    success_url = reverse_lazy('index')


class GenreDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'person_confirm_delete.html'  # TODO genre_confirm_delete.html
    model = Genre
    success_url = reverse_lazy('index')


class CountryModelForm(ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean()
        name = cleaned_data['name'].strip().capitalize()
        return name


class CountryCreateView(LoginRequiredMixin, CreatePopupMixin, CreateView):
    template_name = 'movie_create.html'  # TODO country_create.html
    form_class = CountryModelForm
    success_url = reverse_lazy('index')


class CountryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'country_create.html'
    model = Country
    form_class = CountryModelForm
    success_url = reverse_lazy('index')


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'person_confirm_delete.html'  # TODO country_confirm_delete.html
    model = Country
    success_url = reverse_lazy('index')


def movies(request):
    g = request.GET.get('genre', '')
    c = request.GET.get('country', '')
    genres = Genre.objects.all()
    if g != '' and c != '':
        g = int(g)
        c = int(c)
        if Genre.objects.filter(id=g).exists() and Country.objects.filter(id=c).exists():
            genre = Genre.objects.get(id=g)
            country = Country.objects.get(id=c)
            movie_list = Movie.objects.filter(genres=genre, countries=country)
            context = {'movies': movie_list, 'genres': genres, 'filtered_by': f'podle žánru {genre} a země {country}.'}
            return render(request, 'movies.html', context)
    if g != '':
        g = int(g)
        if Genre.objects.filter(id=g).exists():
            genre = Genre.objects.get(id=g)
            context = {'movies': genre.movies_of_genre.all(), 'genres': genres, 'filtered_by': f'podle žánru {genre}'}
            return render(request, 'movies.html', context)
        else:
            context = {'movies': [], 'genres': genres, 'filtered_by': ''}
            return render(request, 'movies.html', context)

    if c != '':
        c = int(c)
        if Country.objects.filter(id=c).exists():
            country = Country.objects.get(id=c)
            context = {'movies': country.movies_in_country.all(), 'genres': genres,
                       'filtered_by': f'podle země {country}'}
            return render(request, 'movies.html', context)
        else:
            context = {'movies': [], 'genres': genres, 'filtered_by': ''}
            return render(request, 'movies.html', context)

    movies_list = Movie.objects.all()
    genre_list = Genre.objects.all()
    context = {'movies': movies_list, 'genres': genre_list, 'filtered_by': ''}
    return render(request, 'movies.html', context)


def movies_by_genre(request, pk):
    genre_movies = Genre.objects.get(id=pk)
    genre_list = Genre.objects.all()
    context = {'movies': genre_movies.movies_of_genre.all(), 'genres': genre_list}
    return render(request, 'movies.html', context)


def movies_by_country(request, pk):
    country_movies = Country.objects.get(id=pk)
    country_list = Country.objects.all()
    genre_list = Genre.objects.all()
    context = {'movies': country_movies.movies_in_country.all(), 'countries': country_list, 'genres': genre_list}
    return render(request, 'movies.html', context)


class MoviesView(View):
    def get(self, request):
        movies_list = Movie.objects.all()
        context = {'movies': movies_list}
        return render(request, 'movies.html', context)


class MoviesTemplateView(TemplateView):
    template_name = 'movies.html'
    extra_context = {'movies': Movie.objects.all()}


class MoviesListView(ListView):
    template_name = 'movies2.html'
    model = Movie
    paginate_by = 5


def movie(request, pk):
    try:
        movie_obj = Movie.objects.get(id=pk)
    except:
        return render(request, 'index.html')  # TODO: vypsat na vyrenderované stránce chybu

    # spočítat průměrné hodnocení filmu
    avg_rating = None
    if Rating.objects.filter(movie=movie_obj).count() > 0:
        avg_rating = Rating.objects.filter(movie=movie_obj).aggregate(Avg('rating'))

    # hodnocení od daného uživatele
    user = request.user
    user_rating = None
    if request.user.is_authenticated:
        if Rating.objects.filter(movie=movie_obj, user=user).count() > 0:
            user_rating = Rating.objects.get(movie=movie_obj, user=user)

    # komentáře k filmu
    comments = Comment.objects.filter(movie=movie_obj).order_by('-created')

    # obrázky k filmu
    images = Image.objects.filter(movie=movie_obj)

    context = {'movie': movie_obj, 'avg_rating': avg_rating,
               'user_rating': user_rating, 'comments': comments, 'images': images}
    return render(request, 'movie.html', context)


class MovieForm(Form):
    title_orig = CharField(max_length=64)
    title_cz = CharField(max_length=64, required=False)
    title_sk = CharField(max_length=64, required=False)
    countries = ModelMultipleChoiceField(queryset=Country.objects)
    genres = ModelMultipleChoiceField(queryset=Genre.objects, widget=CheckboxSelectMultiple)
    directors = ModelMultipleChoiceField(queryset=Person.objects)
    actors = ModelMultipleChoiceField(queryset=Person.objects)
    year = IntegerField(min_value=1900, max_value=datetime.now().year + 3)
    video = CharField(max_length=128, required=False)
    description = CharField(widget=Textarea, required=False)

    def clean_title_orig(self):
        initial_form = super().clean()
        initial = initial_form['title_orig'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


class MovieModelForm(LoginRequiredMixin, ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

        widgets = {
            'countries': AddAnotherWidgetWrapper(
                SelectMultiple,
                reverse_lazy('country_create')
            )
        }

        labels = {
            'title_orig': 'Originální název'
        }

        help_texts = {
            'title_orig': 'Zadejte originální název'
        }

        error_messages = {
            'title_orig': {
                'max_length': 'Zadaný název je příliš dlouhý'
            }
        }

    def clean_title_orig(self):
        initial_form = super().clean()
        initial = initial_form['title_orig'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


class MovieFormView(LoginRequiredMixin, FormView):
    template_name = 'movie_create.html'
    form_class = MovieForm
    success_url = reverse_lazy('movie_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        new_movie = Movie.objects.create(
            title_orig=cleaned_data['title_orig'],
            title_cz=cleaned_data['title_cz'],
            title_sk=cleaned_data['title_sk'],
            # countries=cleaned_data['countries'],
            # genres=cleaned_data['genres'],
            # directors=cleaned_data['directors'],
            # actors=cleaned_data['actors'],
            year=cleaned_data['year'],
            video=cleaned_data['video'],
            description=cleaned_data['description']
        )
        new_movie.countries.set(cleaned_data['countries'])
        new_movie.genres.set(cleaned_data['genres'])
        new_movie.directors.set(cleaned_data['directors'])
        new_movie.actors.set(cleaned_data['actors'])
        new_movie.save()
        return result

    def form_invalid(self, form):
        print('User provided invalid data.')
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'movie_create.html'
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.add_movie'


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'movie_create.html'
    model = Movie
    form_class = MovieModelForm
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.change_movie'


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'person_confirm_delete.html'  # TODO movie_confirm_delete.html
    model = Movie
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.delete_movie'


@login_required
def persons(request):
    persons_list = Person.objects.all()
    context = {'persons': persons_list}
    return render(request, 'persons.html', context)


class PersonsListView(ListView):
    template_name = 'persons2.html'
    model = Person


def actors(request):
    actors_object = Person.objects.filter(acting_in_movie__isnull=False).distinct()
    directors_objects = Person.objects.filter(directing_movie__isnull=False).distinct()
    context = {'actors': actors_object, 'directors': directors_objects}
    return render(request, 'persons2.html', context)


def actor(request, pk):
    actor_object = Person.objects.get(id=pk)
    context = {'actor': actor_object}
    return render(request, 'person.html', context)


# TODO: vytvořit CBV, která zvlášť zobrazí herce a zvlášť režiséry


def person(request, pk):
    person_obj = Person.objects.get(id=pk)
    context = {'person': person_obj}
    return render(request, 'person.html', context)


class PersonForm(Form):
    first_name = CharField(max_length=32)
    last_name = CharField(max_length=32)
    birth_date = DateField()
    biography = TextField()

    def clean_first_name(self):
        initial_data = super().clean()
        initial = initial_data['first_name']
        return initial.capitalize()

    def clean_last_name(self):
        initial_data = super().clean()
        initial = initial_data['last_name']
        return initial.capitalize()


class PersonModelForm(LoginRequiredMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget = DateInput(
            attrs={
                'type': 'date',
                'placeholder': 'dd-mm-yyyy',
                'class': 'form-control'
            }
        )

    class Meta:
        model = Person
        fields = '__all__'  # ve formuláři budou všechny atributy
        # fields = ['last_name', 'first_name']  # ve formuláři se zobrazí pouze tyto atributy (v daném pořadí)
        # exclude = ['biography']  # ve formuláři budou všechny atributy kromě těchto

    def clean_first_name(self):
        initial_data = super().clean()
        initial = initial_data['first_name']
        return initial.capitalize()

    def clean_last_name(self):
        initial_data = super().clean()
        initial = initial_data['last_name']
        return initial.capitalize()


class PersonFormView(LoginRequiredMixin, FormView):
    template_name = 'person_create.html'
    form_class = PersonModelForm
    success_url = reverse_lazy('person_create')

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Person.objects.create(
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            birth_date=cleaned_data['birth_date'],
            biography=cleaned_data['biography']
        )
        return result

    def form_invalid(self, form):
        print('User provided invalid data.')
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PersonCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'person_create.html'
    form_class = PersonModelForm
    success_url = reverse_lazy('person_create')
    permission_required = 'viewer.add_person'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PersonUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'person_create.html'
    model = Person
    form_class = PersonModelForm
    success_url = reverse_lazy('persons')
    permission_required = 'viewer.change_person'

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PersonDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'person_confirm_delete.html'
    model = Person
    success_url = reverse_lazy('persons')
    permission_required = 'viewer.delete_person'


@login_required
def rate_movie(request):
    user = request.user
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_obj = Movie.objects.get(id=movie_id)
        rating = request.POST.get('rating')

        if rating:
            if Rating.objects.filter(movie=movie_obj, user=user).count() > 0:
                # aktualizujeme hodnocení
                user_rating = Rating.objects.get(movie=movie_obj, user=user)
                user_rating.rating = rating
                user_rating.save()
            else:
                Rating.objects.create(
                    movie=movie_obj,
                    user=user,
                    rating=rating
                )
        # else:
        #    return redirect(f"/movie/{movie_id}/")
    #return redirect(f"/movie/{movie_id}/")
    return redirect('movie', pk=movie_id)



# view pro přidávání komentářů
@login_required
def add_comment(request):
    user = request.user
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_obj = Movie.objects.get(id=movie_id)
        comment = request.POST.get('comment').strip()
        if comment:
            Comment.objects.create(
                movie=movie_obj,
                user=user,
                comment=comment
            )
    #return redirect(f"/movie/{movie_id}")
    return redirect('movie', pk=movie_id)
