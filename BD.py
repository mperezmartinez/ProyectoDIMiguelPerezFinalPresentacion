# -*- coding: utf-8 -*-
from gi.repository import Gtk
import sqlite3 as dbapi
import Venta


class Conexion:
    # Usamos dbapi para acceder a la base de datos y hacemos un cursor de dicha base
    db = dbapi.connect("coches.dat")
    cursor = db.cursor()


    # Metodo que crea la tabla coches en la base de datos con sus parametros y hace commit
    def createTable(self):
        """Creamos la tabla en caso de que no exista y hacemos un commit.

        """
        self.cursor.execute("""create table if not exists coches(id Integer primary key,marca text, modelo text,motor text,cambio text ,puertas Integer ,cilindrada text,
              Año text,precio text,preciov text,fecha DATETIME)""")
        self.db.commit()

    # Metodo para recoger el ultimo id de la base de datos y lo devuelve
    def selectid(self):
        """Hace un select para recoger la ultima id

        :return: Devuelve la ultima id
        """
        self.cursor.execute("""select * from coches""")
        for result in self.cursor:
            ultid = result[0]
        return ultid

    # Metodo que hace select y lo introduce en un TreeView
    def select(self):
        """Hace un select de la tabla coches en la base de datos y los añade el treeView de la Ventana de Venta.

        """

        Venta.Venta.lista.clear()

        self.cursor.execute("""select * from coches""")

        for result in self.cursor:
            Venta.Venta.lista.append(result)

        Venta.Venta.vista.set_model(Venta.Venta.lista)


    # Metodo para insertar en la tabla coches en el que se le pasan los parametros necesarios para la tabla
    def insert(self, id, marca, modelo, ano, motor, cambio, puertas, cilindrada, precio, preciov):
        """Inserta en la base de datos.

        Inserta en la base de datos los elementos que le pasamos y la fecha actual y hace commit.

        :param id: Id del coche introducido
        :param marca: Marca del coche introducido
        :param modelo: Modelo del coche introducido
        :param ano: Año del coche introducido
        :param motor: Motor del coche introducido
        :param cambio: Tipo de Cambio del coche introducido
        :param puertas: Numero de Puertas del coche introducido
        :param cilindrada: Cilindrada del coche introducido
        :param precio: Precio Pagado del coche introducido
        :param preciov: Precio de Venta del coche introducido

        """

        reg = (id, marca, modelo, motor, cambio, puertas, cilindrada, ano, precio, preciov)
        self.cursor.execute("INSERT INTO coches values(?,?,?,?,?,?,?,?,?,?,datetime('now'))", reg)
        self.db.commit()

    # Metodo para borrar el registro pasandole el id asignado
    def delete(self, id):
        """Recoge una id y borra el registro con dicha id de la base de datos.

        Recoge la id que le pasamos y borra el registro con dicha id de la base de datos y hace un commit para guardar los cambios.

        :param id: Id que queremos borrar

        """
        reg = str(id)
        self.cursor.execute("delete from coches where id=?", reg)
        self.db.commit()

    # Metodo para actualizar el precio de la id pasada
    def update(self, id, prez):
        """Cambia el precio de venta del id pasado al nuevo precio pasado.

        :param id: Id del elemento que queremos cambiar el precio
        :param prez: Nuevo precio a introducir.

        """
        reg = (prez, id)
        self.cursor.execute("update coches set preciov=? where id=?", reg)
        self.db.commit()
