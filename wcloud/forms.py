from django import forms

class TextForm(forms.Form):
    text = forms.CharField(error_messages={'required': '请输入文本'},label="",widget=forms.Textarea(attrs={'class':'form-control'}),max_length=100000)
    