from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from datetime import datetime


def printPdf(request, filename, queryset, template):
    html_string = render_to_string('{template}'.format(template=template), {'entities': queryset})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    filename = '{filename}-{date}'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
        filename=filename,
    )

    html.write_pdf(
        target='/tmp/{filename}.pdf'.format(filename=filename),
        stylesheets=[CSS(settings.STATIC_ROOT + '/css/print.css')],
        # presentational_hints=True
    )

    fs = FileSystemStorage('/tmp')
    with fs.open('{filename}.pdf'.format(filename=filename)) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{filename}.pdf"'.format(filename=filename)
        return response

    return response
