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
    webui_props_value = forms.CharField(
        label='WEBUI Props Value',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'cols': '40',
                'rows': '1'
            }
        ),
        required=False
    )