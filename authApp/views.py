from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
#
from steller.exports import exportXlsx
from steller.prints import printPdf
#
from authApp.models import User
from authApp.repository import UserRepository
from authApp.types.UserType import UserCreationForm, UserUpdateForm, UserForm
#
from .types.GroupType import GroupForm


#Perfis de usuários
class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_group'
    model = Group
    template_name = 'group/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Perfil de Usuários'
        context['menu_group'] = 'active'
        return context


class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'auth.add_group'
    model = Group
    form_class = GroupForm
    template_name = 'group/new.html'
    success_message = '%(field)s - criado com sucesso'
    success_url = reverse_lazy('group_index')

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Perfil de Usuários'
        context['menu_group'] = 'active'
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.name,
        )


class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'auth.change_group'
    model = Group
    form_class = GroupForm
    template_name = 'group/edit.html'
    success_message = '%(field)s - editado com sucesso'
    success_url = reverse_lazy('group_index')

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Perfil de Usuários'
        context['menu_group'] = 'active'
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.name,
        )


class GroupDeleteView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'auth.delete_group'
    model = Group
    template_name = 'group/delete.html'
    success_url = reverse_lazy('group_index')

    success_message = 'Deletado com sucesso'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(GroupDeleteView, self).delete(request, *args, **kwargs)
#Fim Perfil de usuários

#Usuários
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'user/index.html'
    paginate_by = 10

    def get_queryset(self):
        new_context = UserRepository.get_query_filter(self.request)
        return new_context

    def get_context_data(self, **kwargs):
        context = UserRepository.get_context(self, UserListView)
        return context


@permission_required('auth.view_user')
def export_users(request):
    model = 'User'
    filename = 'usuarios_exportados'

    queryset = UserRepository.get_query_filter_export(request)

    columns = ('Nome', 'Veículos', 'Data de cadastro', 'Grupos')

    response = exportXlsx(model, filename, queryset, columns)
    return response


@permission_required('auth.view_user')
def print_users(request):
    queryset = UserRepository.get_query_filter(request)
    template = 'user/print.html'
    filename = 'steller-usuários'
    return printPdf(request, filename, queryset, template)


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'auth.add_user'
    model = User
    form_class = UserForm
    template_name = 'user/new.html'
    success_message = '%(field)s - criado com sucesso'
    success_url = reverse_lazy('user_index')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Usuários'
        context['menu_user'] = 'active'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        group = form.cleaned_data['group']
        self.object.groups.clear()
        self.object.groups.add(group)
        self.object.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.name,
        )


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'auth.change_user'
    model = User
    form_class = UserUpdateForm
    template_name = 'user/edit.html'
    success_message = '%(field)s - editado com sucesso'
    success_url = reverse_lazy('user_index')

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            pass
        else:
            initial['group'] = current_group.pk
        return initial

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Usuários'
        context['menu_user'] = 'active'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        #
        group = form.cleaned_data['group']
        self.object.groups.clear()
        self.object.groups.add(group)

        self.object.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.name,
        )

def UserChangePassword(request, pk):
    user = User.objects.get(pk=pk)
    template_name = 'user/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'A senha de {user} foi alterada!'.format(user=user.name))
            return redirect('user_index')
    else:
        form = PasswordChangeForm(user=user)
    context['form'] = form
    context['user'] = user
    return render(request, template_name, context)

class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'auth.delete_user'
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_index')

    success_message = 'Deletado com sucesso'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())