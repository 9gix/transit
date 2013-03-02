from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DirectionForm(forms.Form):
    direction_from = forms.CharField(
        label = "Direction From",
        max_length = 100,
        required = True,
    )
    direction_to = forms.CharField(
        label = "Direction To",
        max_length = 100,
        required = True,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('go', 'Find Bus'))
        super(DirectionForm, self).__init__(*args, **kwargs)

