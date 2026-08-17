import datetime
from django import forms
from .models import House, Todo, Operatiune, Pastoral
from django.utils import timezone

class HouseForm(forms.ModelForm): # ADD HOUSE FORM
    name = forms.CharField(label="Numar(id)")
    leader_year = forms.DateField(
        label="An regina 👑", required=True,
        widget=forms.DateInput(attrs={'type': 'date'})) 
    location = forms.CharField(label="Locatie(optional)", required=False)
    rating = forms.IntegerField(#label="Evaluare(1...5)",
            widget=forms.NumberInput(attrs={
               'min': 1,'max': 5,'step': 1}))   
    history = forms.CharField(label="Detalii 📜", 
           widget=forms.Textarea(attrs={'rows':'3', 'cols':'10'}), required=False)
    class Meta:
        model = House
        exclude = ['user', 'status', 'bifata'] # , 'history'
    def clean_leader_year(self):
        data = self.cleaned_data.get('leader_year')
        #if data != '':
        #    if data > datetime.date.today():
        #        raise forms.ValidationError("⚠️ Data nu poate fi din viitor.")
        return data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = 'Evaluare(1...5 ⭐)' # Adaugă steaua în label
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["leader_year"].initial = timezone.now().date()
        #self.fields["leader_year"].input_formats = ['%d/%m/%Y']

class HouseEditForm(forms.ModelForm): # # EDIT HOUSE FORM
    leader_year = forms.DateField(
        label="An regina 👑 {{ self.instance.leader_year }}", 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    location = forms.CharField(label="Locatie(optional)", required=False)
    rating = forms.IntegerField(#label="Evaluare(1...5)",
            widget=forms.NumberInput(attrs={
               'min': 1,'max': 5,'step': 1}))   
    history = forms.CharField(label="Istoric 📜", 
           widget=forms.Textarea(attrs={'rows':'3', 'cols':'10'}), required=False)
    class Meta:
        model = House
        exclude = ['user', 'name', 'bifata'] # , 'history'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = 'Evaluare(1...5 ⭐)' # Adaugă steaua în label
        if self.instance and self.instance.leader_year:
            self.fields['leader_year'].label=(
                f"An regina ({self.instance.leader_year.strftime('%d-%m-%Y')})"
            )
        
class TodoForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':'5', 'cols':'12'}),
                                  required=False)
    class Meta:
        model = Todo
        fields = ["description"]
        exclude = ['updated_at', 'user']

class OperatiuneForm(forms.ModelForm):
    class Meta:
        model = Operatiune
        fields = ['tip', 'suma', 'descriere']
        widgets = {
            'tip': forms.Select(attrs={
                'class': 'form-select',
            }),
            'suma': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Introduceți suma în lei'
            }),
            'descriere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Salariu, factură electricitate...'
            }),
        }
        labels = {
            'tip': 'Tip operațiune',
            'suma': 'Sumă (lei)',
            'descriere': 'Descriere opțională',
        }

class TreatmentForm(forms.Form):
    data_aplicare = forms.DateField(
        label="Data aplicării", 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    medicament = forms.CharField(
        label="Medicament administrat", 
        max_length=100
    )

class VisitForm(forms.Form):
    data_visita = forms.DateField(
        label="Data", 
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=datetime.date.today
    )
    detalii_visita = forms.CharField(label="Notite(observatii, evenimente - se vor adauga in istoric).", 
        widget=forms.Textarea(attrs={'rows':'3', 'cols':'10'}), required=False)

class PastoralForm(forms.ModelForm):
    data = forms.DateField(
        label="Data plecare", 
        widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today
    ) 
    nr_familii = forms.NumberInput()
    destinatie = forms.CharField(label="Destinatie  ",required=False)
    class Meta:
        model = Pastoral
        fields = ['data', 'nr_familii', 'destinatie']