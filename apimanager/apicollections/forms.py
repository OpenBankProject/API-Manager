from django import forms


class ApiCollectionsForm(forms.Form):
    api_collections_body = forms.CharField(
        label='API Collections Body',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

class ApiCollectionEndpointsForm(forms.Form):
    operation_id = forms.CharField(
        label='Operation Id',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True
    )