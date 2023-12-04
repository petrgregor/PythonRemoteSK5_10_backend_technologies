from django.http import HttpResponse
from django.shortcuts import render

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


def movie(request, pk):
    movie_obj = Movie.objects.get(id=pk)
    context = {'movie': movie_obj}
    return render(request, 'movie.html', context)
