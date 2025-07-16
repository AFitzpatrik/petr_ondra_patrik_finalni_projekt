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
            'start_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['start_date_time', 'end_date_time']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%dT%H:%M')

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