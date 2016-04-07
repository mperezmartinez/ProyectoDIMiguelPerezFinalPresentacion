# -*- coding: utf-8 -*-
import os
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
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

    parrafo = Paragraph("Id,Marca;Modelo,Motor,Cambio,Puertas,Cilindrada,Año,Precio Compra,Precio Venta,Fecha Compra", cabecera)

    guion.append(parrafo)

    bbdd = dbapi.connect("coches.dat")
    cursor = bbdd.cursor()
    cursor.execute("select * from coches")
    taboaBaseDatos = []

    for fila in cursor:
        taboaBaseDatos.append(fila)

    taboa = Table(taboaBaseDatos)


    guion.append(taboa)

    documento = SimpleDocTemplate("BaseCoches.pdf", pagesize=A4, showBoundary=0)
    documento.build(guion)
    cursor.close()