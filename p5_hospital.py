from typing import Any, Protocol


class HospitalError(RuntimeError):
    """Errores en el procesamiento de los datos de la práctica"""
    pass


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


class PrtclSelectorPersona(Protocol):
    """Protocolo para seleccionar personas"""
    
    def es_seleccionable(self, persona: Persona) -> bool:
        """Devuelve True si la persona es seleccionable"""
        ...


class Hospital:
    """Clase que representa un hospital"""
    
    def __init__(self, denominacion: str, *args, **kwargs):
        self.__denominacion = denominacion
        self.__pacientes = {}
        self.__habs_libres = set(range(1, 10))
        self.__habs_ocupadas = set()
    
    def _get_pacientes(self) -> list[Persona]:
        """Obtiene la lista de pacientes"""
        return list(self.__pacientes.values())
    
    def anyadir_paciente(self, paciente: Persona) -> None:
        """Añade un paciente al hospital"""
        dni_lower = paciente.get_dni().lower()
        if dni_lower in self.__pacientes:
            raise HospitalError("Paciente ya está registrado")
        
        self._incorporar_paciente(paciente)
        self.__pacientes[dni_lower] = paciente
    
    def _incorporar_paciente(self, paciente: Persona) -> None:
        """Incorpora un paciente al hospital (asigna habitación)"""
        if not self.__habs_libres:
            raise HospitalError("No hay habitaciones libres")
        
        num_habitacion = min(self.__habs_libres)
        self.__habs_libres.remove(num_habitacion)
        self.__habs_ocupadas.add(num_habitacion)
        
        paciente.set_dato("NumHabitación", num_habitacion)
        paciente.del_dato("Médico")
        paciente.del_dato("Diagnóstico")
    
    def eliminar_paciente(self, dni: str) -> None:
        """Elimina un paciente del hospital"""
        dni_lower = dni.lower()
        if dni_lower not in self.__pacientes:
            raise HospitalError("Paciente no está registrado")
        
        paciente = self.__pacientes.pop(dni_lower)
        self._descartar_paciente(paciente)
    
    def _descartar_paciente(self, paciente: Persona) -> None:
        """Descarta un paciente del hospital (libera habitación)"""
        num_hab = paciente.get_dato("NumHabitación")
        if num_hab:
            self.__habs_ocupadas.remove(num_hab)
            self.__habs_libres.add(num_hab)
        
        paciente.del_dato("NumHabitación")
        paciente.del_dato("Médico")
        paciente.del_dato("Diagnóstico")
    
    def asignar_diagnostico(self, dni: str, nombre_medico: str, diagnostico: str) -> None:
        """Asigna un diagnóstico a un paciente"""
        dni_lower = dni.lower()
        if dni_lower not in self.__pacientes:
            raise HospitalError("Paciente no está registrado")
        
        paciente = self.__pacientes[dni_lower]
        paciente.set_dato("Médico", nombre_medico)
        paciente.set_dato("Diagnóstico", diagnostico)
    
    def seleccionar(self, selector: PrtclSelectorPersona) -> list[Persona]:
        """Selecciona pacientes según criterio"""
        return [p for p in self.__pacientes.values() if selector.es_seleccionable(p)]
    
    def __repr__(self) -> str:
        pacientes_list = [str(p) for p in self.__pacientes.values()]
        return f"({self.__denominacion},\n{pacientes_list})"


def main():
    # 1. Crear hospital
    hospital = Hospital("Hospital-Universitario")
    
    # 2. Crear y añadir personas
    personas_data = [
        ("111", "Iván", 23),
        ("222", "Ana", 22),
        ("333", "Juan", 25),
        ("444", "Eva", 20),
        ("555", "Luis", 21),
        ("666", "Mara", 26),
    ]
    
    for dni, nombre, edad in personas_data:
        persona = Persona(dni, nombre)
        persona.set_dato("Edad", edad)
        hospital.anyadir_paciente(persona)
    
    # 3. Mostrar hospital
    print(hospital)
    
    # 4. Asignar diagnósticos
    diagnosticos = [
        ("111", "Dr. José", "Gripe"),
        ("222", "Dra. Sara", "Catarro"),
        ("333", "Dra. Alba", "Otitis"),
        ("444", "Dr. Abel", "Catarro"),
        ("555", "Dr. José", "Otitis"),
        ("666", "Dra. Alba", "Gripe"),
    ]
    
    for dni, medico, diag in diagnosticos:
        hospital.asignar_diagnostico(dni, medico, diag)
    
    # 5. Mostrar hospital con diagnósticos
    print(hospital)
    
    # 6. Eliminar pacientes
    dnis_a_eliminar = ["111", "333", "555"]
    for dni in dnis_a_eliminar:
        hospital.eliminar_paciente(dni)
    
    # 7. Mostrar hospital final
    print(hospital)


if __name__ == "__main__":
    main()
