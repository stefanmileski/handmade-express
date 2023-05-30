from django import forms
from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, *kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = CustomUser
