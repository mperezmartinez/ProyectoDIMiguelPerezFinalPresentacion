# -*- coding: utf-8 -*-
from gi.repository import Gtk, Gdk
import BD, Venta,Informe
import os



UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menu action='FileNew'>
        <menuitem action='FileNewStandard' />
      </menu>
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditCopy' />
      <menuitem action='EditPaste' />
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNewStandard' />
    <toolitem action='FileQuit' />
  </toolbar>
</ui>
"""


class Ventana:

    bandera=0

    # Instanciamos los elementos necesarios ademas de la interfaz con glade
    builder = Gtk.Builder()
    builder.add_from_file('Interfaz.glade')
    cont=0
    entryMarca = builder.get_object("entryMarca")
    entryModelo = builder.get_object("entryModelo")
    entryAno = builder.get_object("entryAño")
    entryPrecio = builder.get_object("entryPrecio")
    entryCV = builder.get_object("entryCV")
    comboboxMotor = builder.get_object("comboboxtextMotor")
    comboboxCasmbio = builder.get_object("comboboxtextCambio")
    comboboxPuertas = builder.get_object("comboboxtextPuertas")
    entryPreciov = builder.get_object("entryPrecioVenta")

    box = builder.get_object("box1")

    window = builder.get_object('window1')
    action_group = Gtk.ActionGroup("my_actions")
    uimanager = Gtk.UIManager()
    accelgroup =uimanager.get_accel_group()
    uimanager.insert_action_group(action_group)


    def __init__(self):
        """Init de la clase que se ejecuta cada vez que la abrimos.

        Inicializa todo lo necesario para el funcionamiento de la ventana,
        como recoger las señales con los botones ,creacion de la base de datos y como no ,
        mostrar la ventana

        """


        # Hacemos visible la window1 del interfaz y la barra de opciones
        self.window.show_all()

        self.uimanager.add_ui_from_string(UI_INFO)
        self.window.add_accel_group(self.accelgroup)

        self.add_file_menu_actions(self.action_group)
        self.add_edit_menu_actions(self.action_group)

        menubar = self.uimanager.get_widget("/MenuBar")
        toolbar = self.uimanager.get_widget("/ToolBar")

        self.box.pack_start(menubar, False, False, 0)
        self.box.pack_start(toolbar, False, False, 0)

        #No me va singleton

        # class Singleton (object):
        #     instance = None
        #     def __new__(self,cls):
        #         if self.instance is None:
        #             self.instance = object.__new__(self)
        #         return print("hola")
        #
        # #Usage
        # mySingleton1 = Singleton(self.box.pack_start(menubar, False, False, 0))
        # mySingleton2 = Singleton(self.box.pack_start(toolbar, False, False, 0))


        # Asignamos las señales de los botones a metodos
        signals = {"Comprar": self.Comprar,
                   "Buscar": self.Buscar,
                   "gtk_main_quit": Gtk.main_quit}

        # Conectamos las señales
        self.builder.connect_signals(signals)

        # Creamos la tabla en caso de que no exista
        BD.Conexion().createTable()

    # Codigo del boton Compra , recoge los textos de los entry y los combobox en variables , ademas de recoger la ultima id de la base para seguir a partir de ahi , y los añade a la base de datos como un nuevo registro
    def Comprar(self, widget):
        """Se Ejecuta al Pulsar el Boton Comprar,Recoge todos los valores escritos , y los añade a la base de datos.

        Recoge los valores introducidos en marca,modelo,ano,precio,motor,cambio,puertas,CV y precio de venta y los añade a la base de datos , con la id siguiente a la ultima usada, en caso de que
        no haya ninguna id usa la 1.
        Al terminar de insertar , vaciamos todos los recuadros para mas comodiad de una nueva introduccion.


        :param widget: Recoge el boton


        """

        marca = self.entryMarca.get_text()

        modelo = self.entryModelo.get_text()

        ano = self.entryAno.get_text()

        precio = self.entryPrecio.get_text()

        motor = self.comboboxMotor.get_active_text()

        cambio = self.comboboxCasmbio.get_active_text()

        puertas = self.comboboxPuertas.get_active_text()
        int(puertas)

        cv = self.entryCV.get_text()

        preciov = self.entryPreciov.get_text()

        # Recogemos la ultima id con un select y ponemos el contador a ese nivel para que  sea la siguiente id,en caso de que  no haya ningun registro empieza el contador a 1
        try:
            self.cont = BD.Conexion().selectid()
            self.cont = self.cont + 1
        except UnboundLocalError:
            self.cont = self.cont + 1

        BD.Conexion().insert(self.cont, marca, modelo, ano, motor, cambio, puertas, cv, precio, preciov)

        self.entryMarca.set_text("")
        self.entryModelo.set_text("")
        self.entryAno.set_text("")
        self.entryPrecio.set_text("")
        self.entryCV.set_text("")
        self.entryPreciov.set_text("")

    # Codigo del boton buscar, cierra esta ventana  y inicia la otra clase que contiene una segunda interfaz
    def Buscar(self, widget):
        """Se Ejecuta al pulsar el boton buscar , cerrando esta ventana y abriendo la de busqueda.

        :param widget: Recoge el boton

        """
        self.window.hide()
        Venta.Venta().window.show_all()


    #Añade los menu file con sus submenus , y relaciona cada uno con el metodo que ejecuta
    def add_file_menu_actions(self, action_group):
        """Linkea las pestañas de la barra de opciones file con sus utilidades.


        :param action_group: Le pasamos el action grup que tiene las pestañas de la barra

        """

        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenewmenu = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenewmenu)

        action_new = Gtk.Action("FileNewStandard", "Nuevo Informe",
            "Create a new file", Gtk.STOCK_NEW)
        action_new.connect("activate", self.genera_informe)
        action_group.add_action_with_accel(action_new, None)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)


    #Añade los menu edit con sus submenus , y relaciona cada uno con el metodo que ejecuta
    def add_edit_menu_actions(self, action_group):
        """Linkea las pestañas de la barra de opciones edit con sus utilidades.

        :param action_group: Le pasamos el action grup que tiene las pestañas de la barra

        """
        action_group.add_actions([
            ("EditMenu", None, "Edit"),
            ("EditCopy", Gtk.STOCK_COPY, None, None, None,
             self.copypaste),
            ("EditPaste", Gtk.STOCK_PASTE, None, None, None,
             self.copypaste),
        ])


    #Metodo que llama a la clase Informe , genera un informe en pdf y lo muestra
    def genera_informe(self, widget):
        """Genera un informe de la base de datos y nos lo muestra.

        :param widget: Recoge el boton

        """
        Informe.informe()
        os.system("evince BaseCoches.pdf &")
    #Metodo que cierra la aplicacion
    def on_menu_file_quit(self, widget):
        """Al pulsar cierra totalmente la aplicacion.

        :param widget: Recoge el boton

        """
        Gtk.main_quit()

    #Metodo para el copy y paste , indicando que los has seleccionado , ya que no se como hacer que copien y pegen
    def copypaste(self, widget):
        """Cuando pulsamos , nos muestra un texto de has seleccionado con el nombre de lo seleccionado.

        :param widget: Recoge el boton

        """
        print("Has seleccionado : " + widget.get_name() + " ")




if __name__ == '__main__':
    vent = Ventana()
    Gtk.main()