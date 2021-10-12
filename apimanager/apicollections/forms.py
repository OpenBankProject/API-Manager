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