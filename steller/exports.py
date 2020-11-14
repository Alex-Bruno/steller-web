from django.http import HttpResponse
import xlwt
from datetime import datetime


def exportXlsx(model, filename, queryset, columns):
    response = HttpResponse(
        content_type='application/ms-excel',
    )

    filename = '{filename}-{date}.xlsx'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
        filename=filename,
    )

    response['Content-Disposition'] = 'attachment; filename={filename}'.format(
        filename=filename,
    )

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    rows = queryset

    for row, rowdata in enumerate(rows):
        row_num += 1

        for col, val in enumerate(rowdata):
            ws.write(row_num, col, val, default_style)

    wb.save(response)

    return response