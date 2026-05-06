from abc import ABC, abstractmethod
from typing import Protocol


class MediaError(RuntimeError):
    """Errores en el procesamiento de los datos de la práctica"""
    pass


class PrtclCalculoMedia(Protocol):
    """Protocolo para calcular medias"""
    
    def calc_media(self, lista_nums: list[int | float]) -> float:
        """Calcula la media de una lista de números"""
        ...


class Datos:
    """Clase para almacenar y gestionar datos numéricos"""
    
    def __init__(self, *args, **kwargs):
        self.__lista_nums = []
    
    def get_datos(self) -> list[int | float]:
        """Obtiene la lista de números"""
        return self.__lista_nums
    
    def anyadir_datos(self, lista_nums: list[int | float]) -> None:
        """Añade números a la lista"""
        self.__lista_nums.extend(lista_nums)
    
    def eliminar_datos(self, lista_nums: list[int | float]) -> None:
        """Elimina números de la lista"""
        for num in lista_nums:
            if num in self.__lista_nums:
                self.__lista_nums.remove(num)
    
    def calc_media(self, calculadora: PrtclCalculoMedia) -> float:
        """Calcula la media usando una calculadora"""
        return calculadora.calc_media(self.__lista_nums)
    
    def __repr__(self) -> str:
        return f"Datos: {self.__lista_nums}"


class CalculoMediaAbstracto(ABC):
    """Clase abstracta para cálculo de medias"""
    
    @abstractmethod
    def calc_media(self, lista_nums: list[int | float]) -> float:
        """Calcula la media de una lista de números"""
        pass


class MediaAritmetica(CalculoMediaAbstracto):
    """Calcula la media aritmética"""
    
    def calc_media(self, lista_nums: list[int | float]) -> float:
        """Calcula la media aritmética"""
        if not lista_nums:
            raise MediaError("Lista vacía")
        return sum(lista_nums) / len(lista_nums)


class MediaArmonica(CalculoMediaAbstracto):
    """Calcula la media armónica"""
    
    def calc_media(self, lista_nums: list[int | float]) -> float:
        """Calcula la media armónica"""
        nums_positivos = [num for num in lista_nums if num > 0]
        if not nums_positivos:
            raise MediaError("No hay datos válidos")
        return len(nums_positivos) / sum(1 / num for num in nums_positivos)


class MediaTruncada(CalculoMediaAbstracto):
    """Calcula la media truncada dentro de un intervalo"""
    
    def __init__(self, valor_min: float, valor_max: float, *args, **kwargs):
        self.__valor_min = valor_min
        self.__valor_max = valor_max
    
    def calc_media(self, lista_nums: list[int | float]) -> float:
        """Calcula la media de números dentro del intervalo"""
        nums_filtrados = [num for num in lista_nums if self.__valor_min <= num <= self.__valor_max]
        if not nums_filtrados:
            raise MediaError("No hay datos válidos")
        return sum(nums_filtrados) / len(nums_filtrados)


def main():
    # 1. Crear objeto Datos
    datos = Datos()
    
    # 2. Añadir primera lista de números
    datos.anyadir_datos([62, 66, 52, 54, 52, 56, 67, 61, 68, 55, 66, 64, 69, 60, 54, 51, 57, 65, 56, 51])
    
    # 3. Añadir segunda lista de números
    datos.anyadir_datos([35, 78, 45, 67])
    
    # 4. Eliminar números
    datos.eliminar_datos([83, 23, 54, 67, 64])
    
    # 5. Mostrar representación
    print(datos)
    
    # 6. Calcular distintos tipos de media
    media_aritmetica = MediaAritmetica()
    print(f"MediaAritmetica: {datos.calc_media(media_aritmetica):.2f}")
    
    media_armonica = MediaArmonica()
    print(f"MediaArmonica: {datos.calc_media(media_armonica):.2f}")
    
    media_truncada = MediaTruncada(55.0, 65.0)
    print(f"MediaTruncada: {datos.calc_media(media_truncada):.2f}")


if __name__ == "__main__":
    main()
