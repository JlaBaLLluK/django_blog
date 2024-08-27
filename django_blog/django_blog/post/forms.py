from django.forms import ModelForm, Textarea

from post.models import Post


class WritePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')
