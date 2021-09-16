from django import forms
from .models import Collection, CollectionItem


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ('name', 'description', 'photo', 'group')
        description = forms.CharField(max_length=100, widget=forms.Textarea)

    def clean_data(self):
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        if '' in name and '' in description:
            raise forms.ValidationError('Необходимо заполнить данное поле формы!')
        return name, description


class ItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = ('name', 'description', )
        description = forms.CharField(max_length=100, widget=forms.Textarea)

    def clean_data(self):
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        if '' in name and '' in description:
            raise forms.ValidationError('Необходимо заполнить данное поле формы!')
        return name, description
