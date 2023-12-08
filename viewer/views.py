from logging import getLogger

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from viewer.models import *
from django.forms import Form, ModelChoiceField, Textarea, IntegerField, CharField, ModelMultipleChoiceField, \
    CheckboxSelectMultiple, ModelForm, DateField, SelectDateWidget, DateInput

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


def movies(request):
    movies_list = Movie.objects.all()
    context = {'movies': movies_list}
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


def movie(request, pk):
    movie_obj = Movie.objects.get(id=pk)
    context = {'movie': movie_obj}
    return render(request, 'movie.html', context)


class MovieForm(Form):
    title_orig = CharField(max_length=64)
    title_cz = CharField(max_length=64, required=False)
    title_sk = CharField(max_length=64, required=False)
    countries = ModelMultipleChoiceField(queryset=Country.objects)
    genres = ModelMultipleChoiceField(queryset=Genre.objects, widget=CheckboxSelectMultiple)
    directors = ModelMultipleChoiceField(queryset=Person.objects)
    actors = ModelMultipleChoiceField(queryset=Person.objects)
    year = IntegerField(min_value=1900, max_value=2025)
    video = CharField(max_length=128, required=False)
    description = CharField(widget=Textarea, required=False)

    def clean_title_orig(self):
        initial_form = super().clean()
        initial = initial_form['title_orig'].strip()
        return initial.capitalize()

    def clean(self):
        return super().clean()


class MovieCreateView(FormView):
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
            #countries=cleaned_data['countries'],
            #genres=cleaned_data['genres'],
            #directors=cleaned_data['directors'],
            #actors=cleaned_data['actors'],
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


def persons(request):
    persons_list = Person.objects.all()
    context = {'persons': persons_list}
    return render(request, 'persons.html', context)


class PersonsListView(ListView):
    template_name = 'persons2.html'
    model = Person


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


class PersonModelForm(ModelForm):

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
        #fields = ['last_name', 'first_name']  # ve formuláři se zobrazí pouze tyto atributy (v daném pořadí)
        #exclude = ['biography']  # ve formuláři budou všechny atributy kromě těchto

    def clean_first_name(self):
        initial_data = super().clean()
        initial = initial_data['first_name']
        return initial.capitalize()

    def clean_last_name(self):
        initial_data = super().clean()
        initial = initial_data['last_name']
        return initial.capitalize()


class PersonFormView(FormView):
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


class PersonCreateView(CreateView):
    template_name = 'person_create.html'
    form_class = PersonModelForm
    success_url = reverse_lazy('person_create')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PersonUpdateView(UpdateView):
    template_name = 'person_create.html'
    model = Person
    form_class = PersonModelForm
    success_url = reverse_lazy('persons')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)


class PersonDeleteView(DeleteView):
    template_name = 'person_confirm_delete.html'
    model = Person
    success_url = reverse_lazy('persons')
