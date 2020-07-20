from rest_framework import serializers
from news.models import Article, Journalist
from datetime import datetime
from django.utils.timesince import timesince

# class JournalistSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Journalist
#         fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    time_since_publication = serializers.SerializerMethodField()
    # author = serializers.StringRelatedField()
    #author = JournalistSerializer()

    class Meta:
        model = Article
        fields = '__all__'
        #exclude = ['id']
        #fields - __all__ or a list/tupels of fields
        #exclude - all but the list of field to exclude
    
    def get_time_since_publication(self, object):
        #publication_date = object.publication_date
        time_delta = timesince(object.publication_date,now=datetime.now())
        return time_delta

    def validate(self, data):
        """ check the description and title"""
        if data['title'] == data['description']:
            raise serializers.ValidationError('title and description must be different')
        return data

    def validate_title(self, value):
        if len(value) < 10 :
            raise serializers.ValidationError('title must be 10 chr or more')
        return value


class JournalistSerializer(serializers.ModelSerializer):
    #articles = ArticleSerializer(many=True, read_only=True)
    articles = serializers.HyperlinkedRelatedField(many=True,
    read_only=True,
    view_name='article-detail')

    class Meta:
        model = Journalist
        fields = '__all__'

# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     body = serializers.CharField()
#     location = serializers.CharField()
#     publication_date = serializers.DateField()
#     active = serializers.BooleanField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Article.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.body = validated_data.get('body', instance.body)
#         instance.location = validated_data.get('location', instance.location)
#         instance.publication_date = validated_data.get('publication_date', instance.publication_date)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         """ check the description and title"""
#         if data['title'] == data['description']:
#             raise serializers.ValidationError('title and description must be different')
#         return data

#     def validate_title(self, value):
#         if len(value) < 60 :
#             raise serializers.ValidationError('title must be 60 chr or more')
#         return value
