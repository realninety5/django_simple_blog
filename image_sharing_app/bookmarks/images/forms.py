from django.core.files.base import ContentFile
from django.utils.text import slugify
from urllib import request
from .models import Image
from django import forms

# Image creation form created dynamically from models.py
class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    # Cleans the data passed to the form and check if extension is valid
    def clean_url(self):
        url = self.cleaned_data['url']
        extension = url.rsplit('.', 1)[1].lower()
        valid_extensions = ['jpg', 'jpeg']
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid extensions.')
        return url

    # Overrides thw default save() method while we download the image from the bookmarked urls
    def save(self, force_insert=False, false_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # Download image from given URL
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        # If image should be committed, save it
        if commit:
            image.save()
        return image
