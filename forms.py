from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label='',widget=forms.TextInput(
        attrs={
        'class':'search-query form-control',
        'placeholder':'Search'
        }
    ))

class DetectForm(forms.Form):
    msg = forms.CharField(label='Enter Your Message Here', max_length=100)