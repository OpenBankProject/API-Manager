from django import forms


class WebuiForm(forms.Form):

    webui_props = forms.CharField(
        label='WEBUI Props',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )