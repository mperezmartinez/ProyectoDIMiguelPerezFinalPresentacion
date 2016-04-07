from distutils.core import setup

setup(name="Compra-Venta Manolo",
      version="0.1",
      description="Programa de Compra-Venta de coches",
      author="Miguel Perez",
      author_email="mperezmartinez@danielcastelao.org",
      license="GPL",
      scripts=["Main.py"],
      py_modules=["Venta","BD","Informe"]

)