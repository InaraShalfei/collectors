from django import forms
from .models import Collection, CollectionItem, Photo, Comment


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ('name', 'description', 'photo', 'group')
        description = forms.CharField(max_length=100, widget=forms.Textarea)

    def clean_data(self):
        name = self.cleaned_data['name']
        if '' in name:
            raise forms.ValidationError('Необходимо заполнить данное поле формы!')
        return name


class ItemForm(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = ('name', 'description', 'photo', )
        description = forms.CharField(max_length=100, widget=forms.Textarea)
        photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_data(self):
        name = self.cleaned_data['name']
        if '' in name:
            raise forms.ValidationError('Необходимо заполнить данное поле формы!')
        return name


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        text = forms.CharField(max_length=100, widget=forms.Textarea)
