from django import forms
from phone_directory.models import Main, Firstname, Street, Surname, Patronymic

class MainForm(forms.ModelForm):
    class Meta:
        model = Main
        fields = '__all__'

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            instance = kwargs.get('instance')
            if instance:
                for field_name, field in self.fields.items():
                    field.widget.attrs['value'] = getattr(instance, field_name)

class SearchForm(forms.ModelForm):
    class Meta:
        model = Main
        fields = '__all__'

    firstname = forms.ModelChoiceField(
        queryset=Firstname.objects.all(), required=False)
    surname = forms.ModelChoiceField(
        queryset=Surname.objects.all(), required=False)
    patronymic = forms.ModelChoiceField(
        queryset=Patronymic.objects.all(), required=False)
    street = forms.ModelChoiceField(
        queryset=Street.objects.all(), required=False)
    house = forms.CharField(required=False)
    corpus = forms.CharField(required=False)
    apartments = forms.IntegerField(required=False)
    phone = forms.CharField(required=False)
