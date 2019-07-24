from django import forms


class SearchForm(forms.Form):
    key = forms.CharField(max_length=20, min_length=1)
    page = forms.IntegerField(min_value=1)
