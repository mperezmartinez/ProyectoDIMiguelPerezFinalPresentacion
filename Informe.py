# -*- coding: utf-8 -*-
import os
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

import sqlite3 as dbapi


class informe:
    """Clase informe que genera un informe de la base de datos completa cuando queremos.

    """

    hojaEstilo = getSampleStyleSheet()

    guion = []
    cabecera = hojaEstilo['Heading5']
    cabecera.backColor = colors.red

    #parrafo = Paragraph("Id,Marca;Modelo,Motor,Cambio,Puertas,Cilindrada,Año,Precio Compra,Precio Venta,Fecha Compra", cabecera)

    #guion.append(parrafo)

    bbdd = dbapi.connect("coches.dat")
    cursor = bbdd.cursor()
    titulo=["Id","Marca","Modelo","Motor","Cambio","Puertas","Cilindrada","Año","Precio Compra","Precio Venta","Fecha Compra"]
    ventas=list(cursor.execute("select * from coches"))
    taboaBaseDatos = []
    taboaBaseDatos.append(titulo)

    for fila in ventas:
        taboaBaseDatos.append(fila)

    taboa = Table(taboaBaseDatos)


    estilo = TableStyle([('GRID', (0, 0), (-1, -1), 2, colors.white),
                             ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
                             ('BACKGROUND', (0, 0), (-1, 0), colors.grey)])
    taboa.setStyle(estilo)

    guion.append(taboa)

    documento = SimpleDocTemplate("BaseCoches.pdf", pagesize=A4, showBoundary=0)
    documento.build(guion)
    cursor.close()