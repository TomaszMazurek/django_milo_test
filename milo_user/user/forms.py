from .models import MiloUser
from django.forms import ModelForm, DateInput, NumberInput


class DateInput(DateInput):
    input_type = 'date'


class MiloAddForm(ModelForm):
    class Meta:
        model = MiloUser
        fields = ['username', "password", 'birthDate']
        widgets = {
            'birthDate': DateInput(),
        }


class MiloUpdateForm(ModelForm):
    class Meta:
        model = MiloUser
        fields = ['username', "password", 'birthDate', 'number']
        widgets = {
            'birthDate': DateInput(),
        }