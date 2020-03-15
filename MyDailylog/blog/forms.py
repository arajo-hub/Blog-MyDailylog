from django import forms
from .models import Post, Comment

# models.py에서 만든 models들을 import하여 form을 만든다. 만든 form은 views.py에 import되어 사용된다.

class PostForm(forms.ModelForm): # Post를 만드는 form
    class Meta: # class Meta는 Inner class로 사용하여 상위 클래스에 meta data를 제공한다.
        model=Post # model로는 Post를 사용한다.
        fields=('author', 'title', 'text',) # Post모델에서 가져다 사용할 fields

        widgets={
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }
        # dictionary형태. title을 호출하면 title을 입력할 TextInput이 나타나고, text를 호출하면 내용을 입력할 Textarea가 나타난다.

class CommentForm(forms.ModelForm): # comment를 만드는 form
    class Meta:
        model=Comment
        fields=('author', 'text',)

        widgets={
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea-textarea'})
        }
