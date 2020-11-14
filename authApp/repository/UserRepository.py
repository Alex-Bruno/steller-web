from django.db.models import Q
#
from authApp.models import  User
from authApp.types.UserType import FilterUserForm

def get_query(request):
    query = Q(is_active=True)
    if request and request.GET.get('name'):
        name = request.GET.get('name')
        query.add(Q(name__contains=name), Q.AND)

    if request and request.GET.get('group'):
        group = int(request.GET.get('group'))
        if group > 0:
            query.add(Q(groups__pk=group), Q.AND)

    return query

def get_query_filter(request):
    query = get_query(request)

    new_context = User.objects.filter(
        query
    ).order_by('name')

    return new_context

def get_query_filter_export(request):
    query = get_query(request)

    new_context = User.objects.filter(
        query
    ).extra(
        select={
            'date_joined_format': "DATE_FORMAT(authApp_user.date_joined, '%%d/%%m/%%Y %%H:%%i')",
        }
    ).values_list(
        'name',
        'vehicles__plate',
        'date_joined_format',
        'groups__name',
    ).order_by('name')

    return new_context

def get_context(self, instance, **kwargs):
    context = super(instance, self).get_context_data(**kwargs)

    name = ''
    group = None
    if self.request and self.request.GET.get('name'):
        name = self.request.GET.get('name')

    if self.request and self.request.GET.get('group'):
        group = self.request.GET.get('group')

    context['page_name'] = 'Usuários'
    context['menu_user'] = 'active'
    context['form'] = FilterUserForm(initial={
        'name': name,
        'group': group,
    })

    return context