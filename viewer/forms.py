from django import forms
from .models import Event
from django import forms
from .models import Comment

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'type',
            'description',
            'start_date_time',
            'end_date_time',
            'event_image',
            'location',
        ]
        widgets = {
            'start_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Napište komentář...'}),
        }
        labels = {
            'content': '',
        }