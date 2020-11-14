from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserCreationForm, UserChangeForm
from django import forms
#
from authApp.models import User

#
class FilterUserForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Digite o nome",

            }
        ),
        label='Nome',
        required=False
    )

    choices = tuple(Group.objects.all().values_list())

    choices = [(0, 'Selecione um grupo')] + list(choices)
    choices = tuple(choices)

    group = forms.ChoiceField(
        choices=choices,
        label='Grupo',
        required=False
    )


class UserForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                  required=True, label='Grupo')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'group')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exist = User.objects.filter(email=email).exists()

        if self.instance.pk:
            exist = User.objects.filter(email=email).excluded(pk=self.instance.pk).exists()

        if exist:
            raise forms.ValidationError('Este e-mail já está cadastrado, por favor urilize outro.')

        return email


class UserUpdateForm(UserChangeForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True, label='Grupo')

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'group')

    def clean_email(self):

        email = self.cleaned_data.get('email')
        if self.instance.pk:
            exist = User.objects.filter(email=email).first()
            if exist and exist.pk == self.instance.pk:
                exist = False
        else:
            exist = User.objects.filter(email=email).exists()

        if exist:
            raise forms.ValidationError('Este e-mail já está cadastrado, por favor urilize outro.')

        return email

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['password'].help_text = "Senhas brutas não são armazenadas, então não é possível ver a senha deste usuário, mas você pode trocá-la usando <a href=\"../{pk}/change-password\"> este formulário.</a>.".format(pk=self.instance.pk)