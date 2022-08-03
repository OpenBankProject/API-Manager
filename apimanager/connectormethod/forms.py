from django import forms


class ConnectorMethodForm(forms.Form):
    api_collections_body = forms.CharField(
        label='API Collections Body',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

class ConnectorMethodEndpointForm(forms.Form):
    operation_id = forms.CharField(
        label='Operation Id',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True
    )