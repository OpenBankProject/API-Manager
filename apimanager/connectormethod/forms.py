from django import forms


class ConnectorMethodForm(forms.Form):
    connector_method_body = forms.CharField(
        label='Connector Method Body',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

