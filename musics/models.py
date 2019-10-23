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