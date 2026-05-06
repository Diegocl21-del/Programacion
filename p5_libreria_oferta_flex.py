from typing import Protocol
from abc import ABC, abstractmethod


class LibroError(RuntimeError):
    """Errores en el procesamiento de los datos de la práctica"""
    pass


class LibreriaError(RuntimeError):
    """Errores en el procesamiento de librerías"""
    pass


class Libro:
    """Clase que representa un libro"""
    
    def __init__(self, autor: str, titulo: str, precio_base: float, iva: float = 10.0):
        if precio_base < 0:
            raise LibroError("Precio base negativo")
        self.__autor = autor
        self.__titulo = titulo
        self.__precio_base = precio_base
        self.__iva = iva
    
    def get_autor(self) -> str:
        return self.__autor
    
    def get_titulo(self) -> str:
        return self.__titulo
    
    def get_precio_base(self) -> float:
        return self.__precio_base
    
    def get_iva(self) -> float:
        return self.__iva
    
    def set_iva(self, iva: float) -> None:
        self.__iva = iva
    
    def _calc_base_imponible(self) -> float:
        return self.__precio_base
    
    def calc_precio_final(self) -> float:
        base = self._calc_base_imponible()
        return base * (1 + self.__iva / 100)
    
    def __repr__(self) -> str:
        return f"({self.__autor}; {self.__titulo}; {self.__precio_base:.2f}; {self.get_iva():.2f}%; {self.calc_precio_final():.2f})"


class LibroOferta(Libro):
    """Clase que representa un libro con oferta"""
    
    def __init__(self, porc_descuento: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__porc_descuento = porc_descuento
    
    def get_descuento(self) -> float:
        return self.__porc_descuento
    
    def set_descuento(self, porc_descuento: float) -> None:
        self.__porc_descuento = porc_descuento
    
    def _calc_base_imponible(self) -> float:
        base = self.get_precio_base()
        return base * (1 - self.__porc_descuento / 100)
    
    def __repr__(self) -> str:
        return f"({self.get_autor()}; {self.get_titulo()}; {self.get_precio_base():.2f}; {self.__porc_descuento:.2f}%; {self._calc_base_imponible():.2f}; {self.get_iva():.2f}%; {self.calc_precio_final():.2f})"


class Libreria:
    """Clase que representa una librería"""
    
    def __init__(self):
        self.__libros = {}
    
    def _insertar_libro(self, libro: Libro) -> None:
        """Inserta un libro en la librería"""
        autor_lower = libro.get_autor().lower()
        if autor_lower not in self.__libros:
            self.__libros[autor_lower] = {}
        titulo_lower = libro.get_titulo().lower()
        self.__libros[autor_lower][titulo_lower] = libro
    
    def anyadir_libro(self, autor: str, titulo: str, precio_base: float) -> None:
        """Añade un nuevo libro a la librería"""
        libro = Libro(autor, titulo, precio_base)
        self._insertar_libro(libro)
    
    def eliminar_libro(self, autor: str, titulo: str) -> None:
        """Elimina un libro de la librería"""
        autor_lower = autor.lower()
        titulo_lower = titulo.lower()
        
        if autor_lower not in self.__libros or titulo_lower not in self.__libros[autor_lower]:
            raise LibreriaError(f"Libro no encontrado ({autor}, {titulo})")
        
        del self.__libros[autor_lower][titulo_lower]
        if not self.__libros[autor_lower]:
            del self.__libros[autor_lower]
    
    def eliminar_autor(self, autor: str) -> None:
        """Elimina todos los libros de un autor"""
        autor_lower = autor.lower()
        if autor_lower not in self.__libros:
            raise LibreriaError(f"Autor no encontrado ({autor})")
        del self.__libros[autor_lower]
    
    def calc_precio_final(self, autor: str, titulo: str) -> float:
        """Calcula el precio final de un libro"""
        autor_lower = autor.lower()
        titulo_lower = titulo.lower()
        
        if autor_lower not in self.__libros or titulo_lower not in self.__libros[autor_lower]:
            raise LibreriaError(f"Libro no encontrado ({autor}, {titulo})")
        
        return self.__libros[autor_lower][titulo_lower].calc_precio_final()
    
    def __repr__(self) -> str:
        libros_list = []
        for autor_dict in self.__libros.values():
            for libro in autor_dict.values():
                libros_list.append(libro)
        return f"[{', '.join(str(libro) for libro in libros_list)}]"


class PrtclOfertaFlex(Protocol):
    """Protocolo para ofertas flexibles"""
    
    def get_descuento(self, libro: Libro) -> float:
        """Calcula el porcentaje de descuento para un libro"""
        ...


class OfertaFlexAbstracta(ABC):
    """Clase abstracta para ofertas flexibles"""
    
    @abstractmethod
    def get_descuento(self, libro: Libro) -> float:
        """Calcula el porcentaje de descuento para un libro"""
        pass


class OfertaPrecio(OfertaFlexAbstracta):
    """Oferta basada en precio mínimo"""
    
    def __init__(self, porc_descuento: float, umbral_precio: float, *args, **kwargs):
        if porc_descuento < 0:
            raise LibroError("Porcentaje de descuento negativo")
        self.__porc_descuento = porc_descuento
        self.__umbral_precio = umbral_precio
    
    def get_descuento(self, libro: Libro) -> float:
        if libro.get_precio_base() >= self.__umbral_precio:
            return self.__porc_descuento
        return 0.0
    
    def __repr__(self) -> str:
        return f"{self.__porc_descuento:.2f}%({self.__umbral_precio:.2f})"


class OfertaAutor(OfertaFlexAbstracta):
    """Oferta basada en autores específicos"""
    
    def __init__(self, porc_descuento: float, autores_oferta: list[str], *args, **kwargs):
        if porc_descuento < 0:
            raise LibroError("Porcentaje de descuento negativo")
        self.__porc_descuento = porc_descuento
        self.__autores_oferta = {autor.lower() for autor in autores_oferta}
    
    def get_descuento(self, libro: Libro) -> float:
        if libro.get_autor().lower() in self.__autores_oferta:
            return self.__porc_descuento
        return 0.0
    
    def __repr__(self) -> str:
        return f"{self.__porc_descuento:.2f}%{self.__autores_oferta}"


class LibreriaOfertaFlex(Libreria):
    """Librería con ofertas flexibles"""
    
    def __init__(self, oferta_flex: PrtclOfertaFlex, *args, **kwargs):
        super().__init__()
        self.__oferta_flex = oferta_flex
    
    def set_oferta(self, oferta_flex: PrtclOfertaFlex) -> None:
        """Actualiza la oferta flexible"""
        self.__oferta_flex = oferta_flex
    
    def get_oferta(self) -> PrtclOfertaFlex:
        """Obtiene la oferta flexible"""
        return self.__oferta_flex
    
    def anyadir_libro(self, autor: str, titulo: str, precio_base: float) -> None:
        """Añade un nuevo libro con oferta flexible"""
        libro_oferta = LibroOferta(0.0, autor, titulo, precio_base)
        descuento = self.__oferta_flex.get_descuento(libro_oferta)
        
        if descuento > 0:
            libro_oferta.set_descuento(descuento)
            self._insertar_libro(libro_oferta)
        else:
            libro_normal = Libro(autor, titulo, precio_base)
            self._insertar_libro(libro_normal)
    
    def __repr__(self) -> str:
        libros_list = []
        for autor_dict in self._Libreria__libros.values():
            for libro in autor_dict.values():
                libros_list.append(libro)
        return f"({self.__oferta_flex},\n{libros_list})"


def main():
    # 1. Crear LibreriaOfertaFlex con OfertaAutor
    oferta_autor = OfertaAutor(20.0, ["George Orwell", "Isaac Asimov"])
    libreria = LibreriaOfertaFlex(oferta_autor)
    
    # 2. Añadir libros
    libros_a_anyadir = [
        ("george orwell", "1984", 8.20),
        ("Philip K. Dick", "¿Sueñan los androides con ovejas eléctricas?", 3.50),
        ("Isaac Asimov", "Fundación e Imperio", 9.40),
        ("Ray Bradbury", "Fahrenheit 451", 7.40),
        ("Aldous Huxley", "Un Mundo Feliz", 6.50),
        ("xxx", "xxx", -1.00),
        ("Isaac Asimov", "La Fundación", 7.30),
        ("William Gibson", "Neuromante", 8.30),
        ("Isaac Asimov", "Segunda Fundación", 8.10),
        ("Isaac Newton", "arithmetica universalis", 7.50),
        ("George Orwell", "1984", 6.20),
        ("Isaac Newton", "Arithmetica Universalis", 10.50),
    ]
    
    for autor, titulo, precio in libros_a_anyadir:
        try:
            libreria.anyadir_libro(autor, titulo, precio)
        except LibroError as e:
            print(f"Error: {type(e).__name__}('{e}')")
    
    # 3. Mostrar cantidad de libros
    print(f"Cantidad de libros almacenados: {sum(len(d) for d in libreria._Libreria__libros.values())}")
    
    # 4. Mostrar representación de la librería
    libros_list = []
    for autor_dict in libreria._Libreria__libros.values():
        for libro in autor_dict.values():
            libros_list.append(libro)
    print(f"({oferta_autor},")
    print(f"{libros_list})")
    
    # 5. Eliminar libros
    libros_a_eliminar = [
        ("George Orwell", "1984"),
        ("Aldous Huxley", "Un Mundo Feliz"),
        ("xxx", "xxx"),
        ("Isaac Newton", "Arithmetica Universalis"),
        ("Isaac Asimov", "La Fundación"),
    ]
    
    for autor, titulo in libros_a_eliminar:
        try:
            libreria.eliminar_libro(autor, titulo)
        except LibreriaError as e:
            print(f"Error: {type(e).__name__}('{e}')")
    
    # 6. Mostrar cantidad de libros
    print(f"Cantidad de libros almacenados: {sum(len(d) for d in libreria._Libreria__libros.values())}")
    
    # 7. Mostrar representación de la librería
    libros_list = []
    for autor_dict in libreria._Libreria__libros.values():
        for libro in autor_dict.values():
            libros_list.append(libro)
    print(f"({oferta_autor},")
    print(f"{libros_list})")
    
    # 8. Mostrar precios finales
    precios_a_mostrar = [
        ("Philip K. Dick", "¿Sueñan los androides con ovejas eléctricas?"),
        ("isaac asimov", "fundación e imperio"),
        ("Isaac Asimov", "Segunda Fundación"),
        ("Isaac Newton", "Arithmetica Universalis"),
        ("Ray Bradbury", "Fahrenheit 451"),
        ("william gibson", "neuromante"),
    ]
    
    for autor, titulo in precios_a_mostrar:
        try:
            precio = libreria.calc_precio_final(autor, titulo)
            print(f"PrecioFinal({autor}, {titulo}): {precio:.2f}")
        except LibreriaError as e:
            print(f"Error: {type(e).__name__}('{e}')")
    
    # 9. Eliminar autores
    autores_a_eliminar = ["Isaac Asimov", "xxx"]
    
    for autor in autores_a_eliminar:
        try:
            libreria.eliminar_autor(autor)
        except LibreriaError as e:
            print(f"Error: {type(e).__name__}('{e}')")
    
    # 10. Mostrar representación final
    libros_list = []
    for autor_dict in libreria._Libreria__libros.values():
        for libro in autor_dict.values():
            libros_list.append(libro)
    print(f"({oferta_autor},")
    print(f"{libros_list})")


if __name__ == "__main__":
    main()
