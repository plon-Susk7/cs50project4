from .models import Post,Likes
from django.forms import ModelForm,Textarea, fields, widgets

class addPost(ModelForm):
 class Meta:
  model = Post
  fields = ['content']
  widgets = {
   'content': Textarea(attrs={'cols': 80, 'rows': 5})
  }