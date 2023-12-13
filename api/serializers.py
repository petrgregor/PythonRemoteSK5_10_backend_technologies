from rest_framework import serializers

from viewer.models import Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['title_orig', 'year', 'description']


class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'
