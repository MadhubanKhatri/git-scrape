from django import forms

class UserForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter a Username'}),
                                max_length=50, label='')
