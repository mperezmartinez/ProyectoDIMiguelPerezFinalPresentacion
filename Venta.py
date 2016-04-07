# -*- coding: utf-8 -*-
from gi.repository import Gtk
import BD, Main


class Venta:


    sino=0
    # Instanciamos los elementos necesarios ademas de la interfaz con glade
    builder = Gtk.Builder()
    builder.add_from_file('InterfazVenta.glade')

    entryId = builder.get_object("entryID")
    entryprecio = builder.get_object("entryPrecio2")


    lista = Gtk.ListStore(int, str, str, str, str, int, str, str, str, str, str)
    vista = Gtk.TreeView()
    box = builder.get_object("boxselect")
    scroll = Gtk.ScrolledWindow()
    box.add(scroll)
    scroll.add(vista)
    scroll.set_size_request(400, 400)

    window2 = builder.get_object('dialog1')



    def __init__(self):
        """Init de la clase con lo necesario.

        Nos genera el treeView con los registros de la base de datos y con barra lateral,
        muestra la ventana y enlaza las señales de los botones.

        """

        Main.Ventana.bandera=Main.Ventana.bandera+1

        for i, titulos in enumerate(
                ["Id", "Marca", "Modelo", "Motor", "Cambio", "Puertas", "CV", "Año", "Precio Compra", "Precio Venta",
                 "Fecha Compra"]):
            render = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(titulos, render, text=i)
            self.vista.append_column(columna)

        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.scroll.show()

        self.lista.clear()

        # Hacemos visible la window1 del interfaz
        self.window = self.builder.get_object('window1')
        self.window.set_size_request(800,600)
        self.window.show_all()


        # Asignamos las señales de los botones a metodos
        signals = {"Vender": self.Vender,
                   "Volver": self.Volver,
                   "Actualizar": self.Actualizar,
                   "Si": self.si,
                   "No": self.no,
                   "Ok": self.ok,
                   "gtk_main_quit": Gtk.main_quit}

        # Conectamos las señales
        self.builder.connect_signals(signals)

        # Hacemos un select inicial que nos muestra los registros
        BD.Conexion().select()

    # Codigo del boton vender,recogemos el id del elemento seleccionado , borramos el registro con el id pasado , y se hace un select para actualizar la lista
    def Vender(self, widget):
        """Abre la ventana de seguridad para borrar o no un registro


        :param widget: Recoge el boton

        """

        self.window2 .show_all()


    def si(self, widget):
        """Recoge el elemento seleccionado y lo borra de la base de datos.

        Recoge el elemento seleccionado y lo borra de la base de datos y vuelve a hacer un select
        para que se elimine del treeView , en caso de que no se seleccionara ningun vehiculo , sale otra ventana de aviso

        :param widget:  Recoge el boton

        """
        try:
            click = self.vista.get_selection()
            modelo, iterad = click.get_selected()
            if iterad != None:
                id = modelo[iterad][0]

            BD.Conexion().delete(id)
            BD.Conexion().select()

        except UnboundLocalError:
            self.window2.hide()
            self.window3 = self.builder.get_object('dialog2')
            self.window3 .show_all()


        self.window2.hide()

    def ok(self, widget):
        """Despues de un aviso m nos cierra las ventanas emergentes.

        :param widget:  Recoge el boton

        """

        self.window2.hide()
        self.window3.hide()

    def no(self, widget):
        """Cierra la ventana de seguridad , sin eliminar registros.

        :param widget:  Recoge el boton

        """
        self.window2.hide()

    # Codigo del boton volver , ciera esta ventana y reabre la ventana principal
    def Volver(self, widget):
        """Vuelve a la Ventana inicial de Compra.

        Cierra esta ventana y vuelve a abrir la Inicial de Compra , ademas borra el treeView para que la proxima vez que entremos no se duplique

        :param widget: Recoge el Boton

        """

        #Hacer mensaje de esta seguro de que quiere borrar.

        self.window.hide()
        Main.Ventana().window.show_all()
        for i in self.vista.get_columns():
            self.vista.remove_column(i)


    # Codigo del boton actualizar, cambia el precio del coche de la id pasada y actualiza el select
    def Actualizar(self, widget):
        """Recoge el elemento seleccionado y cambia su precio de venta en la base de datos.

        Recogemos el id del elementro seleccionado en el treeView, y el nuevo precio que hemos puesto y actulizamos
        la base de datos con los nuevos datos.
        Hacemos un select para que se vea el nuevo precio en el treeView y vaciamos el recuadro de precio nuevo.

        :param widget: Recoge el boton

        """
        try:
            click = self.vista.get_selection()
            modelo, iterad = click.get_selected()
            if iterad != None:
                id = modelo[iterad][0]

            prez = self.entryprecio.get_text()
            BD.Conexion().update(id, prez)
            BD.Conexion().select()
            self.entryprecio.set_text("")
        except UnboundLocalError:
            self.window3 = self.builder.get_object('dialog2')
            self.window3 .show_all()


if __name__ == '__main__':
    vent = Venta()
    Gtk.main()
