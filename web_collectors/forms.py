from django import forms
from .models import Collection, CollectionItem, Photo, Comment


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ('name', 'description', 'photo', 'group')
        description = forms.CharField(max_length=100, widget=forms.Textarea)

    def clean_data(self):
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        if '' in name:
            raise forms.ValidationError('Необходимо заполнить данное поле формы!')
        return name, description


class ItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = ('name', 'description', 'photo', )
        description = forms.CharField(max_length=100, widget=forms.Textarea)
        photo = forms.MultipleChoiceField()

    def clean_data(self):
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        if '' in name:
            raise forms.ValidationError('Необходимо заполнить данное поле формы!')
        return name, description


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        text = forms.CharField(max_length=100, widget=forms.Textarea)
