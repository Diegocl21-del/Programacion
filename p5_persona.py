from typing import Any


class Persona:
    """Clase que representa una persona"""
    
    def __init__(self, dni: str, nombre: str, *args, **kwargs):
        self.__dni = dni
        self.__nombre = nombre
        self.__datos = {}
    
    def get_dni(self) -> str:
        """Obtiene el DNI"""
        return self.__dni
    
    def get_nombre(self) -> str:
        """Obtiene el nombre"""
        return self.__nombre
    
    def get_dato(self, clave: str) -> Any:
        """Obtiene un dato por clave"""
        clave_lower = clave.lower()
        return self.__datos.get(clave_lower, None)
    
    def set_dato(self, clave: str, valor: Any) -> None:
        """Establece un dato"""
        clave_lower = clave.lower()
        self.__datos[clave_lower] = valor
    
    def del_dato(self, clave: str) -> None:
        """Elimina un dato"""
        clave_lower = clave.lower()
        if clave_lower in self.__datos:
            del self.__datos[clave_lower]
    
    def get_claves(self) -> list[str]:
        """Obtiene las claves de todos los datos"""
        return list(self.__datos.keys())
    
    def __repr__(self) -> str:
        return f"({self.__dni}, {self.__nombre}, {self.__datos})"
    
    def __hash__(self) -> int:
        return hash((self.__dni.lower(), self.__nombre.lower()))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Persona):
            return False
        return (self.__dni.lower() == other.__dni.lower() and 
                self.__nombre.lower() == other.__nombre.lower())
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Persona):
            return NotImplemented
        atrib_self = (self.__dni.lower(), self.__nombre.lower())
        atrib_other = (other.__dni.lower(), other.__nombre.lower())
        return atrib_self < atrib_other
    
    def _atrib_comp(self) -> tuple:
        """Retorna los atributos para comparación"""
        return (self.__dni.lower(), self.__nombre.lower())


def main():
    # 1. Crear persona
    persona1 = Persona("11111111A", "José Luis")
    
    # 2. Añadir datos
    persona1.set_dato("Edad", 25)
    persona1.set_dato("Médico", "Ana María")
    persona1.set_dato("Diagnóstico", "Gripe")
    
    # 3. Mostrar representación
    print(persona1)
    
    # 4. Mostrar dni, nombre y edad
    print(persona1.get_dni())
    print(persona1.get_nombre())
    print(persona1.get_dato("Edad"))
    
    # 5. Eliminar dato y mostrar representación
    persona1.del_dato("médico")
    print(persona1)
    
    # 6. Crear segunda persona y comparar
    persona2 = Persona("11111111a", "josé luis")
    if persona1 == persona2:
        print("Las dos personas son iguales")
    else:
        print("Las dos personas son distintas")


if __name__ == "__main__":
    main()
