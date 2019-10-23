# 직렬화.... 자바 시스템 내붕서 사용되는 object 또는 data를 외부의 자바 시스템에서도 사용할 수 있도록 byte 형태로 데이터를 변환하는 기술
from rest_framework import serializers as sr
from .models import Music, Artist, Comment


# 이렇게 하면 json 파일 형식으로 형변환 해준다.
class MusicSerializer(sr.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist_id',]


class ArtistSerializer(sr.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name',]


class ArtistDetailSerializer(ArtistSerializer):
    musics = MusicSerializer(many=True)

    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + ['musics', ]


class CommentSerializer(sr.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'music_id',  'content',]