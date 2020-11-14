from django.db.models import Q
from datetime import datetime, timedelta
#
from authApp.models import User
from accessApp.models import Access, Vehicle
from accessApp.types.AccessType import FilterAccessForm


def get_query(request):
    query = Q(active=True)
    if request and request.GET.get('plate'):
        plate = request.GET.get('plate')
        query.add(Q(plate__contains=plate), Q.AND)

    if request and request.GET.get('user') and int(request.GET.get('user')) > 0:
        user = request.GET.get('user')
        query.add(Q(vehicle__user=user), Q.AND)

    if request.user.has_perm('accessApp.view_access') == False:
        query.add(Q(vehicle__user=request.user), Q.AND)

    if request and request.GET.get('start_date'):
        start_date = request.GET.get('start_date')
        date = datetime.strptime(start_date, "%d/%m/%Y")
        query.add(Q(entrance__gte=date.date()), Q.AND)

    if request and request.GET.get('start_date_exit'):
        start_date_exit = request.GET.get('start_date_exit')
        date = datetime.strptime(start_date_exit, "%d/%m/%Y")
        query.add(Q(entrance__lte=date.date()+timedelta(days=1)), Q.AND)

    if request and request.GET.get('end_date'):
        end_date = request.GET.get('end_date')
        date = datetime.strptime(end_date, "%d/%m/%Y")
        query.add(Q(exit__gte=date.date()), Q.AND)

    if request and request.GET.get('end_date_exit'):
        end_date_exit = request.GET.get('end_date_exit')
        date = datetime.strptime(end_date_exit, "%d/%m/%Y")
        query.add(Q(exit__lte=date.date()+timedelta(days=1)), Q.AND)

    if request and request.GET.get('not_exit'):
        query.add(Q(exit__isnull=True), Q.AND)

    return query

def get_query_today():
    query = Q(active=True)

    start_date = datetime.now().date()
    start_date_exit = datetime.now().date()

    if start_date:
        query.add(Q(entrance__gte=start_date), Q.AND)

    if start_date_exit:
        query.add(Q(entrance__lte=start_date_exit + timedelta(days=1)), Q.AND)

    new_context = Access.objects.filter(
        query
    ).order_by('-entrance')

    return new_context

def get_query_not_exit():
    new_context = Access.objects.filter(
        exit__isnull=True
    ).order_by('-entrance')

    return new_context

def get_query_filter(request):
    query = get_query(request)
    new_context = Access.objects.filter(
        query
    ).order_by('-entrance')

    return new_context

def get_query_export(request):
    query = get_query(request)

    new_context = Access.objects.filter(
        query
    ).extra(
        select={
            'entrance_format': "DATE_FORMAT(accessApp_access.entrance, '%%d/%%m/%%Y %%H:%%i')",
            'exit_format': "DATE_FORMAT(accessApp_access.exit, '%%d/%%m/%%Y %%H:%%i')",
        }
    ).values_list(
        'plate',
        'vehicle__user__name',
        'entrance_format',
        'exit_format',
    ).order_by('-entrance')

    return new_context


def get_context(self, instance, **kwargs):
    context = super(instance, self).get_context_data(**kwargs)

    user = None
    plate = None
    start_date = None
    start_date_exit = None
    end_date = None
    end_date_exit = None
    not_exit = None

    if self.request and self.request.GET.get('plate'):
        plate = self.request.GET.get('plate')

    if self.request and self.request.GET.get('user'):
        user = self.request.GET.get('user')

    if self.request and self.request.GET.get('start_date'):
        start_date = self.request.GET.get('start_date')

    if self.request and self.request.GET.get('start_date_exit'):
        start_date_exit = self.request.GET.get('start_date_exit')

    if self.request and self.request.GET.get('end_date'):
        end_date = self.request.GET.get('end_date')

    if self.request and self.request.GET.get('end_date_exit'):
        end_date_exit = self.request.GET.get('end_date_exit')

    if self.request and self.request.GET.get('not_exit'):
        not_exit = self.request.GET.get('not_exit')

    context['page_name'] = 'Acessos'
    context['menu_access'] = 'active'

    context['form'] = FilterAccessForm(initial={
        'start_date': start_date,
        'start_date_exit': start_date_exit,
        'end_date': end_date,
        'end_date_exit': end_date_exit,
        'user': user,
        'plate': plate,
        'not_exit': not_exit,
    })

    return context

def get_context_today(self, instance, **kwargs):
    context = super(instance, self).get_context_data(**kwargs)

    start_date = datetime.now().date()
    start_date_exit = datetime.now().date()

    context['page_name'] = 'Acessos'
    context['menu_access'] = 'active'

    context['form'] = FilterAccessForm(initial={
        'start_date': start_date,
        'start_date_exit': start_date_exit,
    })

    return context

def get_context_not_exit(self, instance, **kwargs):
    context = super(instance, self).get_context_data(**kwargs)

    not_exit = True

    context['page_name'] = 'Acessos'
    context['menu_access'] = 'active'

    context['form'] = FilterAccessForm(initial={
        'not_exit': not_exit,
    })

    return context