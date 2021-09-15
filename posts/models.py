from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    text = models.TextField(verbose_name = "Текст")
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts") #on_delete=models.CASCADE если автор будет удален, то удаляться все комменты
    group = models.ForeignKey("Group", on_delete=models.CASCADE, verbose_name = "Группа", blank=True, null=True)
    #поле для картинки
    image = models.ImageField(upload_to='posts/media/', blank=True, null=True)

    
class Group(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name ='Комментарий', related_name = 'comments')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name ='comments')
    text = models.TextField(max_length=500, help_text = 'Текст')
    created = models.DateTimeField("date published", auto_now_add=True)


class Follow(models.Model):
    #который подписывается
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name ='follower')
    #на которого подписываются
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name ='following')

    #class Meta:
        #unique_together = ['user', 'author']