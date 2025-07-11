from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import DateField, NumberInput, CharField, Textarea

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

        labels = {
            'username': 'Uživatelské jméno',
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'E-mail',
            'password1': 'Heslo',
            'password2': 'Heslo znovu'
        }
        
        widgets = {
            'username': CharField().widget,
            'first_name': CharField().widget,
            'last_name': CharField().widget,
            'email': CharField().widget,
            'password1': CharField().widget,
            'password2': CharField().widget,
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs = {'class': 'form-control'}

    date_of_birth = DateField(
        widget=NumberInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Datum narození',
        required=False
    )

    phone = CharField(
        label='Telefon',
        required=False
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)

        date_of_birth = self.cleaned_data.get('date_of_birth')
        biography = self.cleaned_data.get('biography')
        phone = self.cleaned_data.get('phone')
        profile = Profile(
            user=user,
            date_of_birth=date_of_birth,
            biography=biography,
            phone=phone
        )
        if commit:
            profile.save()
        return user
