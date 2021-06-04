from django import forms
from board.models import Boards

from django_summernote.widgets import SummernoteWidget

class BoardsForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class':'sample',
                'placeholder':'제목을 입력해주세요.'
            }
        )
    )
    class Meta:
        model = Boards
        fields = ['title', 'content', 'thumbnail']
        widgets={
            'content': SummernoteWidget(),
        }