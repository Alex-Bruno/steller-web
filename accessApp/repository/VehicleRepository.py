from django.db.models import Q
#
from accessApp.models import Vehicle
from accessApp.types.VehicleType import FilterVehicleForm


def get_query(request):
    query = Q(active=True)
    if request and request.GET.get('plate'):
        plate = request.GET.get('plate')
        query.add(Q(plate__contains=plate), Q.AND)

    if request and request.GET.get('user') and int(request.GET.get('user')) > 0:
        user = request.GET.get('user')
        query.add(Q(user=user), Q.AND)

    if request.user.has_perm('accessApp.view_vehicle') == False:
        query.add(Q(user=self.request.user), Q.AND)

    return query


def get_query_filter(request):
    query = get_query(request)

    new_context = Vehicle.objects.filter(
        query
    ).order_by('plate')

    return new_context


def get_query_filter_export(request):
    query = get_query(request)

    new_context = Vehicle.objects.filter(
        query
    ).values_list(
        'plate',
        'user__name',
        'description',
    ).order_by('plate')

    return new_context


def get_context(self, instance, **kwargs):
    context = super(instance, self).get_context_data(**kwargs)

    plate = ''
    user = None
    if self.request and self.request.GET.get('plate'):
        plate = self.request.GET.get('plate')

    if self.request and self.request.GET.get('user'):
        user = self.request.GET.get('user')

    context['page_name'] = 'Veículos'
    context['menu_vehicle'] = 'active'
    context['form'] = FilterVehicleForm(initial={
        'plate': plate, 'user': user
    })
    return context
