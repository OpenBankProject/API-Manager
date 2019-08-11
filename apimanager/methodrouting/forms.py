from django import forms


class MethodRoutingForm(forms.Form):
    method_routing_body = forms.CharField(
        label='Method Routing Body',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )