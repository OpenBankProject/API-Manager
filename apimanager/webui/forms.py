from django import forms


class WebuiForm(forms.Form):
    webui_props_name = forms.CharField(
        label='WEBUI Props Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    webui_props = forms.CharField(
        label='WEBUI Props',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )