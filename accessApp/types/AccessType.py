from django import forms
from steller import settings
from datetime import datetime
#
from  authApp.models import User
from accessApp.models import Vehicle, Access
from steller.Validators import validatePlate

class FilterAccessForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterAccessForm, self).__init__(*args, **kwargs)

        choices = [(user.pk, user.get_full_name())
                   for user in User.objects.filter(is_active=True)]

        choices = [(0, 'Selecione um usuário')] + list(choices)
        choices = tuple(choices)

        self.fields['user'] = forms.ChoiceField(choices=choices, label='Usuário')

    start_date = forms.DateField(
        input_formats=["%d/%m/%Y"],
        label='De',
        widget=forms.DateInput(attrs={
            'class': 'datepicker',
            'autocomplete': 'off'
        }),
        required=False,
    )

    start_date_exit = forms.DateField(
        input_formats=["%d/%m/%Y"],
        label='Até',
        widget=forms.DateInput(attrs={
            'class': 'datepicker',
            'autocomplete': 'off'
        }),
        required=False,
    )

    end_date = forms.DateField(
        input_formats=["%d/%m/%Y"],
        label='De',
        widget=forms.DateInput(attrs={
            'class': 'datepicker',
            'autocomplete': 'off'
        }),
        required=False,
    )

    end_date_exit = forms.DateField(
        label='Até',
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class': 'datepicker',
            'autocomplete': 'off',
        }),
        required=False,
    )

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

    not_exit = forms.BooleanField(label='Veículos na instituição?', required=False)

class CrateAccessForm(forms.ModelForm):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.filter(active=True),
                                     required=False, label='Veículo')

    entrance = forms.TimeField(input_formats=["%H:%M:%S"], label='Entrada')

    def clean_entrance(self):
        entrance = self.cleaned_data.get('entrance')
        date_str = datetime.now().strftime("%d/%m/%Y")
        entrance = date_str+" "+entrance.strftime("%H:%M:%S")
        entrance = datetime.strptime(entrance, "%d/%m/%Y %H:%M:%S")
        return entrance

    def clean_plate(self):
        plate = self.cleaned_data.get('plate')
        if plate:
            plate = plate.upper()

        if plate and not validatePlate(plate):
            raise forms.ValidationError(
                'Esta placa é inválida, por favor utilize o padrão AAA-1111.')

        return plate

    class Meta:
        model = Access
        fields = ('plate', 'vehicle', 'entrance')

class AccessForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccessForm, self).__init__(*args, **kwargs)
        exit = datetime.now()
        if self.instance.exit:
            exit = self.instance.exit
        print(exit)
        self.initial['exit'] = exit

    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.filter(active=True),
                                     required=False, label='Veículo')

    entrance = forms.TimeField(input_formats=["%H:%M:%S"], label='Entrada', required=True)
    exit = forms.TimeField(input_formats=["%H:%M:%S"], label='Saída', required=False)

    def clean_entrance(self):
        entrance = self.cleaned_data.get('entrance')
        date_str = self.instance.entrance.strftime("%d/%m/%Y")
        entrance = date_str+" "+entrance.strftime("%H:%M:%S")
        entrance = datetime.strptime(entrance, "%d/%m/%Y %H:%M:%S")
        return entrance

    def clean_exit(self):
        exit = self.cleaned_data.get('exit')
        if exit:
            if self.instance.exit:
                date_str = self.instance.exit.strftime("%d/%m/%Y")
            else:
                date_str = datetime.now().strftime("%d/%m/%Y")
            exit = date_str+" "+exit.strftime("%H:%M:%S")
            exit = datetime.strptime(exit, "%d/%m/%Y %H:%M:%S")
        return exit

    def clean_vehicle(self):
        plate = self.cleaned_data.get('plate')
        vehicle = self.cleaned_data.get('vehicle')
        if (not vehicle or int(vehicle.pk) == 0) and plate:
            vehicle = Vehicle.objects.filter(plate=plate).first()
        return vehicle

    def clean_plate(self):
        plate = self.cleaned_data.get('plate').upper()

        if plate and not validatePlate(plate):
            raise forms.ValidationError(
                'Esta placa é inválida, por favor utilize o padrão AAA-1111.')

        return plate

    class Meta:
        model = Access
        fields = ('plate', 'vehicle', 'entrance', 'exit')
