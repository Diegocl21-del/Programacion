from abc import ABC, abstractmethod


class LibroError(RuntimeError):
    """Errores en el procesamiento de los datos de la práctica"""
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


def main():
    # 1. Crear un libro
    libro = Libro("George Orwell", "1984", 6.20)
    print(f"Libro: {libro}")
    
    # 2. Crear una oferta por precio y mostrar descuento
    oferta_precio = OfertaPrecio(20.0, 5.5)
    print(f"Oferta-Precio: {oferta_precio.get_descuento(libro):.2f}")
    
    # 3. Crear una oferta por autor y mostrar descuento
    oferta_autor = OfertaAutor(10.0, ["george orwell", "isaac asimov"])
    print(f"Oferta-Autor: {oferta_autor.get_descuento(libro):.2f}")


if __name__ == "__main__":
    main()
