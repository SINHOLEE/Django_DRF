# rest API

GET : 

POST : 작성해달라는 요청

PUT : 수정하고 싶은 필드가 좁더라도, 그 필드를 가지고 있는 전체를 수정한 파일을 담아 요청을 보냄(수정하고 싶은 정보를 가지고 있는 json 전부 수정)

PATCH : 수정하고자 하는 필드만 데이터에 담아서 요청을 보냄 

DELETE : 삭제

# DRF

1. venv 가상환경

   ```bash
   $ venv
   $ python -m venv venv
   $ python -m pip install --upgrade pip
   $ pip install Django
   ```

2. start project

   ```bash
   $ django-admin startproject api .
   ```

3. 새로운 모듈 설치 : 장고에서 api서버를 만들게 하는 프레임 워크 설치

   ```bash
   $ pip install djangorestframework
   ```

   - DRF = Django Rest api Framework

4. settings.py/installed_apps

   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
   ]
   
   ```

5. musics app 생성

   ```bash
   $ python manage.py startapp musics
   ```

6. settings.py 에 등록

   ```python
   INSTALLED_APPS = [
   
       # Local apps
       'musics',
       
       ......
   ]
   ```

   - 이제는 말할 수 있다. : 사실 등록하는 이름은 `musics.apps. MusicsConfig`로 등록하는 것이 정확하나, 내부에서 이름을 지정하여 앱 이름으로 통일하여 등록가능.

7. musics/models.py

   ```python
   from django.db import models
   
   # Create your models here.
   class Artist(models.Model):
       name = models.CharField(max_length=50)
   
       def __str__(self):
           return self.name
   
   # Artist와 1:N 관계 생성
   class Music(models.Model):
       artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='musics')
       title = models.CharField( max_length=250)
       
       def __str__(self):
           return self.title
   
   
   # Music과 1:N구조인 Comments 생성
   class Comment(models.Model):
       music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='comments')
       content = models.TextField()
       
       def __str__(self):
           return f'{ self.music.pk }번 음악의 {self.pk}번 댓글'
   ```

8. model 등록

   ```bash
   $ python manage.py makemigrations
   $ python manage.py migrate
   $ python manage.py createsuperuser
   ```

9. musics/admin.py

   ```python
   from django.contrib import admin
   from .models import Artist, Music, Comment
   
   
   admin.site.register(Artist)
   admin.site.register(Music)
   admin.site.register(Comment)
   ```

   - 각 모델을 admin으로 추적하겠다.

10. 더미 json 생성

    ```bash
    $ python manage.py dumpdata --indent 2 musics > dummy.json
    ```

11. musics/fixtures 폴더 생성 후 더미파일 생성

12. 더미데이터 삽입

    ```bash
    $ python manage.py loaddata dummy.json
    ```

13. urls.py

    ```python
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('musics/', views.music_list, name='music_list'),
        path('artists/', views.artist_list, name='artist_list'),
        path('comments/', views.comment_list, name='comment_list'),
    
    ]
    
    ```

    - 다음과 같이 각 모델을 생성한다.

14. views.py

    ```python
    from django.shortcuts import render
    from .models import Music, Artist, Comment
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer
    
    @api_view(['GET']) 
    def music_list(request):
        musics = Music.objects.all()   
        serializer = MusicSerializer(musics, many=True)  
        return Response(serializer.data)  
    
    ```

    - `@api_view(['GET']) ` :  어떤 메소드로 처리 될것인지 미리 설정한다.

       `from rest_framework.decorators import api_view`임포트 필요

    - `musics = Music.objects.all()` :  Music 모델이 가지고 있는 모든 정보를 받아오는 객체를 생성한다. 이 객체는 파이썬에서만 읽을 수 있으므로 여러 플랫폼에서 사용하기 위해서는 `json형식`의 파일이 필요하다. 

    - `json`형태로 변화시키기 위해 `serializers.py` 생성하고 15. 과정을 수행한다.

    - `from .serializers import MusicSerializer` : 15 과정을 수행한 뒤 **직렬화**를 위해 임포트 한다.

    - `serializer = MusicSerializer(musics, many=True)` :  `model`을 통해 불러온 객체가 첫번째 인자, 두번째 인자는 만약 그 인자의 원소가 두 개 이상일 경우에는 `many=True` 설정, 하나면 제거한다.

    - `return Response(serializer.data)` : 응답할 때, `serializer`로 변환한 데이터를 `Response`라는 함수에 담아 반환한다.

      `from rest_framework.response import Response` 필요

15. musics.serializers.py 생성

    ```python
    from rest_framework import serializers as sr
    from .models import Music, Artist, Comment
    
    
    class MusicSerializer(sr.ModelSerializer):
        class Meta:
            model = Music
            fields = ['id', 'title', 'artist_id',]
    
    
    class ArtistSerializer(sr.ModelSerializer):
        class Meta:
            model = Artist
            fields = ['id', 'name',]
    
    class CommentSerializer(sr.ModelSerializer):
        class Meta:
            model = Comment
            fields = ['id', 'music_id',  'content',]
    ```

    - 직렬화 :  자바 시스템 내붕서 사용되는 `object` 또는 `data`를 외부의 자바 시스템에서도 사용할 수 있도록 `byte` 형태로 데이터를 변환하는 기술
    - `forms.py`를 사용하듯이, `model`을 `import` 하고, `from rest_framework import serializers`를 임포트 한다.
    - class화 한 각 모델의 serializer를 views.py에 사용한다.

16. 번외 ) 문서화를 위해 drf-yasg 서드파티를 다운받자.

    ```bash
    $ pip install drf-yasg
    ```

17. settings.py에 서드파티 등록한다.

    ```python
    'drf_yasg'
    ```

    

18. musics/urls.py

    ```python
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    
    schema_view = get_schema_view(
        openapi.Info(
            title='Music API',
            default_version='v1',
            description='음악 관련 API 서비스입니다.',
        )
    )
    
    urlpatterns = [
    	......
    
        path('docs/', schema_view.with_ui('redoc'), name='api_docs'),
        path('swagger/', schema_view.with_ui('swagger'), name='api_swagger'),
    ]
    
    ```

    - 문서화를 알아서 해주는 서드파디 모듈이다. 

19. 각 객체의 pk값을 이용해 하나만 가져오기.( artist의 경우만 본다.)

20. urls.py

    ```python
        path('artists/<int:artist_pk>/', views.artist_detail, name='artist_detail'),
    
    ```

21. serializers.py 수정

    ```python
    class ArtistSerializer(sr.ModelSerializer):
        class Meta:
            model = Artist
            fields = ['id', 'name',]
    
    
    class ArtistDetailSerializer(ArtistSerializer):
        musics = MusicSerializer(many=True)
    
        class Meta(ArtistSerializer.Meta):
            fields = ArtistSerializer.Meta.fields + ['musics', ]
    
    ```

    - 첫번째 클래스만 사용할 경우, `json` 파일 자체는 `artist` 정보 자체(가벼움)만 불러올 때 용이하다.
    - 아래 클래스는 아티스트의 곡들까지 전부 반환할 때 필요, 데이터가 상대적으로 무겁다.

22. views.py

    ```python
    @api_view(['GET'])
    def artist_detail(request, artist_pk):
        artist = get_object_or_404(Artist, pk=artist_pk)
        serializer = ArtistDetailSerializer(artist)
        return Response(serializer.data)
    
    ```

    - 하나의 json 파일만 반환하므로, `many=True`변수를 뺀다.