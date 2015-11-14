from django import forms
from .models import Address, Project

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('__all__')
        widgets = {
            'street': forms.TextInput(attrs= {
                'placeholder': '1037 Lawrence St'
                }),
            'city': forms.TextInput(attrs= {
                'placeholder': 'Port Townsend'
                }),
            'state': forms.TextInput(attrs= {
                'placeholder': 'WA'
                }),
            }

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'address')
        widgets = {
            'name': forms.TextInput(attrs = {
                'placeholder':'Doe: Home'
                }),
            'description': forms.TextInput(attrs = {
                'placeholder':'Build a new home for John Doe.'
                }),
            }
        labels = {
            'name': "Name your Project",
            }
        help_texts = {
            'address': "Ctrl-click to select multiple."
            }
