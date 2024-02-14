"""
URL configuration for hollymovie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import rest_framework
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

import accounts.views
import api
from api.views import *
from accounts.views import SignUpView
from viewer.admin import MovieAdmin
from viewer.models import *
from viewer.views import *


# zde budeme vytvářet cesty
urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello', hello),
    path('hello2/<s>', hello2),
    path('hello3/', hello3),
    path('hello4/', hello4),
    path('hello5/<s0>', hello5),

    path('', index, name='index'),

    path('accounts/login/', LoginView.as_view(), name='login'),    # vlastní view
    path('accounts/signup/', SignUpView.as_view(), name='signup'),  # vlastní view
    path('accounts/', include('django.contrib.auth.urls')),      # defaultní views pro přihlašování/odhlašování/změnu hesla...

    path('country/create/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<pk>/', CountryDeleteView.as_view(), name='country_delete'),

    path('genre/create/', GenreCreateView.as_view(), name='genre_create'),
    path('genre/update/<pk>/', GenreUpdateView.as_view(), name='genre_update'),
    path('genre/delete/<pk>/', GenreDeleteView.as_view(), name='genre_delete'),

    #path('movies/', movies, name='movies'),
    #path('movies/', MoviesView.as_view(), name='movies'),
    #path('movies/', MoviesTemplateView.as_view(), name='movies'),
    path('movies/', MoviesListView.as_view(), name='movies'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<pk>/', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<pk>/', MovieDeleteView.as_view(), name='movie_delete'),
    path('movie_detail/<pk>/', movie, name='movie'),

    #path('persons/', persons, name='persons'),
    #path('persons/', PersonsListView.as_view(), name='persons'),  # FIXME: zobrazit zvlášť herce a zvlášť režiséry
    path('persons/', actors, name='persons'),
    #path('person/create/', PersonFormView.as_view(), name='person_create'),
    path('person/create/', PersonCreateView.as_view(), name='person_create'),
    path('person/update/<pk>/', PersonUpdateView.as_view(), name='person_update'),
    path('person/delete/<pk>/', PersonDeleteView.as_view(), name='person_delete'),
    path('person/<pk>/', person, name='person'),  # FIXME

    path('rate_movie/', rate_movie, name='rate_movie'),
    path('add_comment', add_comment, name='add_comment'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/movies/', api.views.Movies.as_view()),
    path('api/movie/<pk>/', api.views.MovieDetail.as_view()),
    path('api/persons/', api.views.PersonsList.as_view()),
    path('api/person/<pk>/', api.views.PersonDetail.as_view()),

    path('profiles/', accounts.views.ProfileListView.as_view(), name='profiles'),
    # path('profile/<pk>/', accounts.views.)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
