from django import forms
from voting.models import (
    Province,
    Locality,
    Zone,
    PoliticalParty,
    Vote
)

class DniForm(forms.Form):
    dni = forms.CharField(label="DNI", max_length=8, min_length=7)



class VoterPreloadForm(forms.Form):
    dni = forms.IntegerField(
        label='DNI',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 12345678'
        })
    )
    first_name = forms.CharField(
        label='Nombre',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        })
    )
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        label='Provincia',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    locality = forms.ModelChoiceField(
        queryset=Locality.objects.none(),
        label='Localidad',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    zone = forms.ModelChoiceField(
        queryset=Zone.objects.none(),
        label='Zona',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    birth_date = forms.DateField(
        label='Fecha de Nacimiento', 
        widget=forms.DateInput(attrs={'type': 'date'}))


    def __init__(self, *args, **kwargs):
        """
        Inicializa los queryset dinámicos para localidades y zonas según provincia y localidad seleccionadas
        """
        super().__init__(*args, **kwargs)

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['locality'].queryset = Locality.objects.filter(province_id=province_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['locality'].queryset = Locality.objects.none()

        if 'locality' in self.data:
            try:
                locality_id = int(self.data.get('locality'))
                self.fields['zone'].queryset = Zone.objects.filter(locality_id=locality_id).order_by('name')
            except (ValueError, TypeError):
                self.fields['zone'].queryset = Zone.objects.none()

class VoteForm(forms.Form):
    type = forms.ChoiceField(
        label='Tipo de voto',
        choices=Vote.TypeVote.choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    political_party = forms.ModelChoiceField(
        queryset=PoliticalParty.objects.all(),
        required=False,
        label='Partido político',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        vote_type = cleaned_data.get('type')
        party = cleaned_data.get('political_party')

        if vote_type == Vote.TypeVote.AFIRMATIVO and not party:
            self.add_error('political_party', 'Debe seleccionar un partido político para un voto afirmativo.')
        elif vote_type != Vote.TypeVote.AFIRMATIVO and party:
            self.add_error('political_party', 'No debe seleccionar un partido si el voto no es afirmativo.')

        return cleaned_data