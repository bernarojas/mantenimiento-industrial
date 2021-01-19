"""
            #from django.db import connection
            #cursor = connection.cursor()
            #cursor.execute('SELECT "Velocidad" FROM "predecirFotos_sensores"')
            #datosRadar22 =cursor.fetchall()

MemIndicesextremosclimaticos.objects.filter(codigoano=año).filter(codigoestacion=codigoEstacion).delete()

          maxRotation: 90,
          minRotation: 90,
#if "buscar" in request.POST:
if request.method == 'POST':

    (datosExcel[:,1], datosExcel[:,2])
    print("VIENDO DATOS:", datosExcel[0].Presion_agua_sello)
    print("VIENDO DATOS:", datosExcel[0].Presion_agua_sello_num)

#   if request.method == 'POST':
#        print("INTENTANDO")
#
#        if request.FILES["datosExcel"]:
#            print("Estoy en if POST")
#            return render(request, 'resultadosExcel.html')
#
#        else:
#            print("AHHHHHHHHHHHHHH")
#            return render(request, 'resultadosExcel.html')

def CargaWebExcel(request):
        #Sensores_excel.objects.all().delete()

        #if request.POST.get['Buscar']:

        #jquery = request.GET['buscar']
        #GuardarEquipos=EQUIPOSCOLOSO(Nombre_equipo='BBA 501 - 503 - 504', Descripcion='ESP3 - Baja Densidad - BBA 501, 503 Y 504',
        #                               Tipo_equipo='PTO.BOMBA')
        #GuardarEquipos.save()

        #wb = load_workbook(filename = 'C:/Users/56975/Pictures/Puerto_Coloso/Bombas densidad baja/543/543.xlsx')
        #if request.FILES["datosExcel"]:

        #print(wb.sheetnames) Nombres de las hojas


        for e in range(2, 4):
                    print( sheet_obj.cell(row = e, column = 1).value.strftime('%d-%m-%Y %H:%M'), 
                                                        sheet_obj.cell(row = e, column = 2).value,
                                                        sheet_obj.cell(row = e, column = 3).value,
                                                        sheet_obj.cell(row = e, column = 4).value,
                                                        sheet_obj.cell(row = e, column = 5).value,
                                                        sheet_obj.cell(row = e, column = 6).value,
                                                        sheet_obj.cell(row = e, column = 7).value,)


        for e in range(1, numeroFilas+1):
                    GuardarSensoresExcel=Sensores_excel( Fecha = sheet_obj.cell(row = e, column = 1).value, 
                                                        Funcionando = sheet_obj.cell(row = e, column = 2).value,
                                                        Presion_agua_sello = sheet_obj.cell(row = e, column = 3).value,
                                                        Flujo_agua_sello = sheet_obj.cell(row = e, column = 4).value,
                                                        Velocidad = sheet_obj.cell(row = e, column = 5).value,
                                                        Flujo_transmisor = sheet_obj.cell(row = e, column = 6).value,
                                                        Densimetro_nuclear = sheet_obj.cell(row = e, column = 7).value,
                                                        Temperatura = 0, Aceleracion = 0, Velocidad_vibracion = 0, 
                                                        Equipo1_id= 1)
                    GuardarSensoresExcel.save()

                                Excel = request.POST["pasando"]
            print(Excel)
            print(request.POST['buscar'])
            #fecha = datetime.strptime(request.POST['buscar'], '%d-%m-%Y %H:%M').datetime()
            fecha = datetime.strptime(request.POST['buscar'], '%d-%m-%Y %H:%M')
            print(fecha)
        """

        #datetime.datetime.strftime(tiempo, '%d-%m-%Y %H:%M').date():
                    #pylint: disable=E1101

        #print("Filas")

        #for e in range(1, numeroFilas+1):
            #cell_obje_row= sheet_obj.cell(row = e, column = 1)
            #print(cell_obje_row.value)

        #return HttpResponseRedirect('resultadosExcel')
        #return render(request, 'resultadosExcel.html', {'datosExcel':datosExcel})