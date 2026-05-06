import re
from abc import ABC, abstractmethod


class IndiceAbstracto(ABC):
    """Clase abstracta para índices de palabras"""
    
    def __init__(self, *args, **kwargs):
        self.__texto = []
    
    def anyadir_frase(self, frase: str) -> None:
        """Añade una frase transformada al texto"""
        # Reemplazar caracteres que no sean letras ni números por espacios
        frase_transformada = re.sub(r'[^a-zA-Z0-9]', ' ', frase)
        self.__texto.append(frase_transformada)
    
    def _get_texto(self) -> list[str]:
        """Obtiene el texto (lista de frases)"""
        return self.__texto
    
    @abstractmethod
    def crear_indice(self) -> None:
        """Método abstracto para crear el índice"""
        pass


class IndiceContador(IndiceAbstracto):
    """Índice que cuenta las apariciones de cada palabra"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__indice_contador = {}
    
    def crear_indice(self) -> None:
        """Crea el índice de contadores"""
        self.__indice_contador.clear()
        
        for frase in self._get_texto():
            palabras = frase.split()
            for palabra in palabras:
                palabra_lower = palabra.lower()
                if palabra_lower:
                    self.__indice_contador[palabra_lower] = self.__indice_contador.get(palabra_lower, 0) + 1
    
    def __repr__(self) -> str:
        lines = []
        for palabra in sorted(self.__indice_contador.keys()):
            lines.append(f"{palabra}: {self.__indice_contador[palabra]}")
        return "\n".join(lines)


class IndiceLineas(IndiceAbstracto):
    """Índice que registra las líneas donde aparece cada palabra"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__indice_lineas = {}
    
    def crear_indice(self) -> None:
        """Crea el índice de líneas"""
        self.__indice_lineas.clear()
        
        for num_linea, frase in enumerate(self._get_texto()):
            palabras = frase.split()
            for palabra in palabras:
                palabra_lower = palabra.lower()
                if palabra_lower:
                    if palabra_lower not in self.__indice_lineas:
                        self.__indice_lineas[palabra_lower] = set()
                    self.__indice_lineas[palabra_lower].add(num_linea)
    
    def __repr__(self) -> str:
        lines = []
        for palabra in sorted(self.__indice_lineas.keys()):
            lineas_sorted = sorted(list(self.__indice_lineas[palabra]))
            lines.append(f"{palabra}: {lineas_sorted}")
        return "\n".join(lines)


class IndicePosicionesLineas(IndiceAbstracto):
    """Índice que registra líneas y posiciones de cada palabra"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__indice_pos_lineas = {}
    
    def crear_indice(self) -> None:
        """Crea el índice de posiciones y líneas"""
        self.__indice_pos_lineas.clear()
        
        for num_linea, frase in enumerate(self._get_texto()):
            palabras = frase.split()
            for posicion, palabra in enumerate(palabras):
                palabra_lower = palabra.lower()
                if palabra_lower:
                    if palabra_lower not in self.__indice_pos_lineas:
                        self.__indice_pos_lineas[palabra_lower] = {}
                    if num_linea not in self.__indice_pos_lineas[palabra_lower]:
                        self.__indice_pos_lineas[palabra_lower][num_linea] = set()
                    self.__indice_pos_lineas[palabra_lower][num_linea].add(posicion)
    
    def __repr__(self) -> str:
        lines = []
        for palabra in sorted(self.__indice_pos_lineas.keys()):
            lines.append(f"{palabra}:")
            for num_linea in sorted(self.__indice_pos_lineas[palabra].keys()):
                posiciones_sorted = sorted(list(self.__indice_pos_lineas[palabra][num_linea]))
                lines.append(f"{num_linea}: {posiciones_sorted}")
        return "\n".join(lines)


def main():
    # Frases del programa
    frases = [
        "Guerra tenía una jarra y Parra tenía una perra, pero la perra de",
        "Parra rompió la jarra de Guerra.",
        "Guerra amarró a la perra de Parra. ¡Oiga usted buen",
        "hombre de Guerra! Por qué ha amarrado a la perra de Parra.",
        "Porque si la perra de Parra no hubiera roto la jarra de Guerra,",
        "Guerra no hubiera amarrado a la perra de Parra."
    ]
    
    # Crear los tres índices
    indice_contador = IndiceContador()
    indice_lineas = IndiceLineas()
    indice_posiciones = IndicePosicionesLineas()
    
    # Añadir frases a los índices
    for frase in frases:
        indice_contador.anyadir_frase(frase)
        indice_lineas.anyadir_frase(frase)
        indice_posiciones.anyadir_frase(frase)
    
    # Crear los índices
    indice_contador.crear_indice()
    indice_lineas.crear_indice()
    indice_posiciones.crear_indice()
    
    # Mostrar resultados
    print("----------------------------")
    print("IndiceContador:")
    print("----------------------------")
    print(indice_contador)
    
    print("\n----------------------------")
    print("IndiceLineas:")
    print("----------------------------")
    print(indice_lineas)
    
    print("\n----------------------------")
    print("IndicePosicionesLineas:")
    print("----------------------------")
    print(indice_posiciones)


if __name__ == "__main__":
    main()
