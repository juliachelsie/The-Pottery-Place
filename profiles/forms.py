from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone': 'Phone Number',
            'default_country': 'Country',
            'default_post_code': 'Postal Code',
            'default_city': 'Town or City',
            'default_address': 'Street Address',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'border-black profile-form-input'
                self.fields[field].label = False