from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from viewer.models import *


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




