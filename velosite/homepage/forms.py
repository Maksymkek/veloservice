from django.forms import TextInput, ModelForm, ImageField, Textarea, NumberInput

from .models import BicycleStation, Bicycle


class VeloStationForm(ModelForm):
    class Meta:
        model = BicycleStation
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Velogroup name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for kw in kwargs:
            self.fields['name'].initial = kwargs[kw].name


class BicycleForm(ModelForm):
    photo = ImageField()

    class Meta:
        model = Bicycle
        fields = ['photo', 'name', 'description', 'usages', 'price']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Bike name'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'usages': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Usages'}),
            'price': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for kw in kwargs:
            self.fields['name'].initial = kwargs[kw].name
            self.fields['usages'].initial = kwargs[kw].usages
            self.fields['description'].initial = kwargs[kw].description
            self.fields['photo'].initial = kwargs[kw].photo
            self.fields['price'].initial = kwargs[kw].price

