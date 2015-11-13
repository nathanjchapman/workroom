from django import forms
from .models import Address, Project

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
