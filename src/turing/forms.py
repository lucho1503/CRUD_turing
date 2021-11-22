from django import forms

class SubmitFile(forms.Form):
	title = forms.CharField(max_length=20)
	file = forms.FileField(allow_empty_file=False)