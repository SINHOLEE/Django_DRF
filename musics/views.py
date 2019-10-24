from django.shortcuts import render, get_object_or_404
from .models import Music, Artist, Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer
# Create your views here.

@api_view(['GET'])  # 어떤 메소드로 처리 될것인지 미리 설정한다.
def music_list(request):
    # /musics?artist_pk=1 했을 때 일번 가수의 모든 음악을 가져와라.라는 명령을 구현할것이다.
    # 만약 artist_pk가 query params로 넘어 온다면, artist_pk로 필터링 한 값만 응답한다.
    params = {}
    artist_pk = request.GET.get('artist_pk')
    if artist_pk is not None:
        params['artist_id'] = artist_pk
    
    musics = Music.objects.filter(**params)  # **dict 형식의 모든 값은 filter에 넣겠다. ( pk=article_pk)

    # -------------------------------------------------------------------------------------------------------------
    
    # musics = Music.objects.all()  # 이 객체는 파이썬에서만 읽을 수 있다. 이를 json 형태의 파일로 바꾸자 이를 위해 DRF가 필요하다.
    # json형태로 변화시키기 위해 serializers.py 생성한다.
    serializer = MusicSerializer(musics, many=True)  # model을 통해 불러온 객체가 첫번째 인자, 두번째 인자는 만약 그 인자의 원소가 두개 이상일 경우에는 many=True 설정 하나면 제거
    return Response(serializer.data)  # 응답할 때, serializer로 변환한 데이터를 Response라는 함수에 담아 반환한다.

# 음악 하나 가져오는거 만들기
@api_view(['GET', 'PUT', 'DELETE'])
def music_detail_update_delete(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    if request.method == "GET":
    # 하나만  가져올때는 many옵션을 쓰면 안된다.
    # 이러한 정보는 협업을 위해 문서화 해야한다.
        serializer = MusicSerializer(music)
    elif request.method == 'DELETE':
        music.delete()
        return Response({'messages' : 'music has been deleted'})
    else:
        serializer = MusicSerializer(data=request.data, instance=music)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    return Response(serializer.data)



@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def artist_detail_update_delete(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    if request.method == "GET":
        serializer = ArtistDetailSerializer(artist)
    elif request.method == 'DELETE':
        artist.delete()
        return Response({'messages' : 'artist has been deleted'})
    else:
        serializer = ArtistSerializer(data=request.data, instance=artist)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    return Response(serializer.data)




@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def comments_create(request, music_pk):
    # Form 같은게 필요할거같긴한데... 어떻게 해야할지 모르겠다. 하지만 POST요청인 것은 자명하다.
    # print(request.data)
    serializer = CommentSerializer(data=request.data)  # 사용자가 보낸 데이터를(request.data)를 CummentSerializer에게 보내겠다.
    if serializer.is_valid(raise_exception=True):  # raise_exception : 검증에 실패하면 400 bad Request 오류를 발생한다. 
        serializer.save(music_id=music_pk)  # Form과는 다르게 commit=False 안해도 된다.
    return Response(serializer.data)
    

@api_view(['PUT', 'DELETE'])
def comments_update_and_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method =='PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    else: # DELETE method로 들어왔다는 뜻.
        comment.delete()
        return Response({'message': 'Comment has been deleted'})