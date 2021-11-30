from django import forms
from multiupload.fields import MultiImageField, MultiMediaField

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
        fields = ('name', 'description' )
        description = forms.CharField(max_length=100, widget=forms.Textarea)
    photos = MultiMediaField(min_num=1, max_num=5, max_file_size=1024*1024*5, media_type='image')

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
