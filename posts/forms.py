from django.forms import ModelForm
from .models import Post, Comment, Follow


#форма создания нового поста
class PostForm(ModelForm):
    class Meta:# эта форма будет работать с моделью Book post
        model = Post
        # на странице формы будут отображаться поля:
        fields = ['text', 'group', 'image']
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


# class FollowForm(ModelForm):
#     class Meta:
#         model = Follow
#         labels = {
#             'user': ('Пользователь подписываеться на:'),
#             'author': ('Автор записи')
#         }

#         help_texts = {
#             'user': ('2Вы подписываетесь на:'),
#             'author': ('2Автор записи'),
#         }

#         fields = ['user', 'author']