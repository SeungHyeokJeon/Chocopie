from django import forms
from board.models import Boards

from django_summernote.widgets import SummernoteWidget

class BoardsForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class':'titlewrite',
                'placeholder':'제목을 입력해주세요.',
            }
        )
    )
    # thumbnail = forms.FileField(
    #     required=False,
    #     widget=forms.FileInput(
    #         attrs={
    #             'class':'fileupload',
    #         }
    #     )
    # )

    class Meta:
        model = Boards
        # fields = ['title', 'content', 'thumbnail']
        fields = ['title', 'content']
        widgets={
            'content': SummernoteWidget(),
        }