from django.shortcuts import render, get_object_or_404
from .models import Music, Artist, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer
# Create your views here.

@api_view(['GET'])  # 어떤 메소드로 처리 될것인지 미리 설정한다.
def music_list(request):
    musics = Music.objects.all()  # 이 객체는 파이썬에서만 읽을 수 있다. 이를 json 형태의 파일로 바꾸자 이를 위해 DRF가 필요하다.
    # json형태로 변화시키기 위해 serializers.py 생성한다.
    serializer = MusicSerializer(musics, many=True)  # model을 통해 불러온 객체가 첫번째 인자, 두번째 인자는 만약 그 인자의 원소가 두개 이상일 경우에는 many=True 설정 하나면 제거
    return Response(serializer.data)  # 응답할 때, serializer로 변환한 데이터를 Response라는 함수에 담아 반환한다.

# 음악 하나 가져오는거 만들기
@api_view(['GET'])
def music_detail(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    # 하나만  가져올때는 many옵션을 쓰면 안된다.
    # 이러한 정보는 협업을 위해 문서화 해야한다.
    serializer = MusicSerializer(music)
    return Response(serializer.data)

@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistDetailSerializer(artists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    serializer = ArtistDetailSerializer(artist)
    return Response(serializer.data)


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)