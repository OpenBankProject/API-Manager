from django import forms


class DynamicEndpointsForm(forms.Form):
    dynamic_endpoints_body = forms.CharField(
        label='Dynamic Endpoints Body',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )