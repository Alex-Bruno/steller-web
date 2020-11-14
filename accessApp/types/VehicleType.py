from django import forms
from steller import settings
#
from authApp.models import User
from accessApp.models import Vehicle, Access
from steller.Validators import validatePlate


class FilterVehicleForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(FilterVehicleForm, self).__init__(*args, **kwargs)

        choices = [(user.pk, user.get_full_name())
                   for user in User.objects.filter(is_active=True)]

        choices = [(0, 'Selecione um usuário')] + list(choices)
        choices = tuple(choices)

        self.fields['user'] = forms.ChoiceField(choices=choices, label='Usuário')

    plate = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Digite a placa",

            }
        ),
        label='Placa',
        required=False
    )

    user = forms.ChoiceField(
        choices=[],
        label='Usuário',
        required=False
    )


class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['plate'].widget.attrs['readonly'] = True

    class Meta:
        model = Vehicle
        fields = ('plate', 'user', 'description')

    def clean_plate(self):
        plate = self.cleaned_data.get('plate').upper()
        if self.instance.pk:
            plate = self.instance.plate
            exist = Vehicle.objects.filter(plate=plate).first()
            if exist and exist.pk == self.instance.pk:
                exist = False
        else:
            exist = Vehicle.objects.filter(plate=plate).exists()

        if exist:
            raise forms.ValidationError(
                'Esta placa já está cadastrada, por favor utilize outra.')

        if not validatePlate(plate):
            raise forms.ValidationError(
                'Esta placa é inválida, por favor utilize o padrão AAA-1111.')

        return plate
