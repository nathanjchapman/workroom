from django import forms
from .models import Door, Code

class CodeForm(forms.ModelForm):

    class Meta:
        model = Code
        fields = ('number', 'permanent', 'belongs_to', 'door')
        widgets = {
            'belongs_to': forms.TextInput(attrs = {
                'placeholder':'John Doe'
                }),
            }
        labels = {
            'permanent': "This is a permanent code"
            }
        help_texts = {
            'door': "Ctrl-click to select multiple."
            }
