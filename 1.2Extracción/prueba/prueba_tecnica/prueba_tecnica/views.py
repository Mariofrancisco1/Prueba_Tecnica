import csv
from django.http import HttpResponse
from .models import data_prueba_tecnica  

def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="datos.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Compañía', 'Monto', 'Estado', 'Creado en', 'Pagado en'])

    transacciones = data_prueba_tecnica.objects.all().values_list('id', 'name', 'company_id', 'amount', 'status', 'created_at', 'paid_at')
    for transaccion in transacciones:
        writer.writerow(transaccion)

    return response
