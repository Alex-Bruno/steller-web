from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
# Export XLSX
from steller.exports import exportXlsx
from steller.prints import printPdf
# My Files
from .models import Vehicle, Access
from accessApp.types.VehicleType import VehicleForm
from accessApp.types.AccessType import CrateAccessForm, AccessForm
from accessApp.repository import VehicleRepository
from accessApp.repository import AccessRepository


# Vehicle
class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicle/index.html'
    paginate_by = 10

    def get_queryset(self):
        new_context = VehicleRepository.get_query_filter(self.request)
        return new_context

    def get_context_data(self, **kwargs):
        context = VehicleRepository.get_context(self, VehicleListView)
        return context


@login_required
def export_vehicles(request):
    model = 'Vehicle'
    filename = 'veiculos_exportados'

    queryset = VehicleRepository.get_query_filter_export(request)

    columns = ('Placa', 'Dono', 'Descrição')

    response = exportXlsx(model, filename, queryset, columns)
    return response


@login_required
def print_vehicles(request):
    queryset = VehicleRepository.get_query_filter(request)
    template = 'vehicle/print.html'
    filename = 'steller-veículos'
    return printPdf(request, filename, queryset, template)


class VehicleCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'accessApp.add_vehicle'
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicle/new.html'
    success_message = '%(field)s - criado com sucesso'
    success_url = reverse_lazy('vehicle_index')

    def get_context_data(self, **kwargs):
        context = super(VehicleCreateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Veículos'
        context['menu_vehicle'] = 'active'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.plate,
        )

    def form_valid(self, form):
        self.object = form.save()
        plate = self.object.plate
        Access.objects.filter(plate=plate).update(vehicle=self.object.pk)
        return super(VehicleCreateView, self).form_valid(form)


class VehicleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'accessApp.change_vehicle'
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicle/edit.html'
    success_message = '%(field)s - editado com sucesso'
    success_url = reverse_lazy('vehicle_index')

    def get_context_data(self, **kwargs):
        context = super(VehicleUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Veículos'
        context['menu_vehicle'] = 'active'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.plate,
        )

class VehicleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'accessApp.delete_vehicle'
    model = Vehicle
    template_name = 'vehicle/delete.html'
    success_url = reverse_lazy('vehicle_index')

    success_message = 'Deletado com sucesso'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


# End Vehicle

# Access
class AccessListView(LoginRequiredMixin, ListView):
    model = Access
    template_name = 'access/index.html'
    paginate_by = 10

    def get_queryset(self):
        new_context = AccessRepository.get_query_filter(self.request)
        return new_context

    def get_context_data(self, **kwargs):
        context = AccessRepository.get_context(self, AccessListView)
        return context

class AccessTodayListView(LoginRequiredMixin, ListView):
    model = Access
    template_name = 'access/index.html'
    paginate_by = 10

    def get_queryset(self):
        new_context = AccessRepository.get_query_today()
        return new_context

    def get_context_data(self, **kwargs):
        context = AccessRepository.get_context_today(self, AccessTodayListView)
        return context

class AccessNotExitListView(LoginRequiredMixin, ListView):
    model = Access
    template_name = 'access/index.html'
    paginate_by = 10

    def get_queryset(self):
        new_context = AccessRepository.get_query_not_exit()
        return new_context

    def get_context_data(self, **kwargs):
        context = AccessRepository.get_context_not_exit(self, AccessNotExitListView)
        return context

@login_required
def export_access(request):
    model = 'Access'
    filename = 'acessos_exportados'

    queryset = AccessRepository.get_query_export(request)

    columns = ('Placa', 'Usuário', 'Entrada', 'Saída')

    response = exportXlsx(model, filename, queryset, columns)
    return response


@login_required
def print_access(request):
    queryset = AccessRepository.get_query_filter(request)
    template = 'access/print.html'
    filename = 'steller-acessos'
    return printPdf(request, filename, queryset, template)


class AccessCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'controllerApp.add_access'
    model = Access
    form_class = CrateAccessForm
    template_name = 'access/new.html'
    success_message = '%(field)s - criado com sucesso'
    success_url = reverse_lazy('access_index')

    def get_context_data(self, **kwargs):
        context = super(AccessCreateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Acessos'
        context['menu_access'] = 'active'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.plate,
        )

    def form_valid(self, form):
        self.object = form.save()
        self.object.isCreatedManual = True
        plate = self.object.plate
        vehicle = self.object.vehicle
        if (vehicle and int(vehicle.pk) > 0) and not plate:
            plate = vehicle.plate
        self.object.plate = plate.upper()
        self.object.save()
        return super(AccessCreateView, self).form_valid(form)

    def get_initial(self):
        entrance = datetime.now()
        return {
            'entrance': entrance,
        }


class AccessUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'controllerApp.change_access'
    model = Access
    form_class = AccessForm
    template_name = 'access/edit.html'
    success_message = '%(field)s - editado com sucesso'
    success_url = reverse_lazy('access_index')

    def get_context_data(self, **kwargs):
        context = super(AccessUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = 'Acessos'
        context['menu_access'] = 'active'
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.isUpdatedManual = True
        plate = self.object.plate
        vehicle = self.object.vehicle
        if (vehicle and int(vehicle.pk) > 0) and not plate:
            plate = vehicle.plate
        self.object.plate = plate.upper()
        self.object.save()
        return super(AccessUpdateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            field=self.object.plate,
        )
