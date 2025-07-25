from datetime import date

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import DateField, NumberInput, CharField, Textarea

from accounts.models import Profile

# Registrační formulář, rozšiřuje vestavěný UserCreationForm
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Fieldy, které chci zobrazit ve formuláři
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

        # Popisky pro jednotlivá pole na stránce
        labels = {
            'username': 'Uživatelské jméno: ',
            'first_name': 'Jméno: ',
            'last_name': 'Příjmení: ',
            'email': 'E-mail: ',
            'password1': 'Heslo: ',
            'password2': 'Heslo znovu: '
        }
        
        # Pro určení vzhledu v bootstrapu 
        widgets = {
            'username': CharField().widget,
            'first_name': CharField().widget,
            'last_name': CharField().widget,
            'email': CharField().widget,
            'password1': CharField().widget,
            'password2': CharField().widget,
        }
        
    # Po spuštení formuláře bude vše v bootstrapu
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs = {'class': 'form-control'}

    
    date_of_birth = DateField(
        widget=NumberInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Datum narození: ',
        required=False
    )


    phone = CharField(
        label='Telefon: ',
        required=False
    )

    # Clean metoda pro datum narození - nesmí být v budoucnosti
    def clean_date_of_birth(self):
        initial = self.cleaned_data['date_of_birth']
        if initial and initial > date.today():
            raise ValidationError('Datum narození nesmí být v budoucnosti.')
        return initial

    # Uloží uživatele
    @atomic
    def save(self, commit=True):
        self.instance.is_active = True  # uživatel je po registraci aktivní
        user = super().save(commit)

        # Získání dalších údajů z formuláře
        date_of_birth = self.cleaned_data.get('date_of_birth')
        biography = self.cleaned_data.get('biography')
        phone = self.cleaned_data.get('phone')
        
        # Vytvoří profil uživatele
        profile = Profile(
            user=user,
            date_of_birth=date_of_birth,
            biography=biography,
            phone=phone
        )
        if commit:
            profile.save()
        return user
