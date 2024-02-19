import random
import time
from Proceso import Proceso

class Planificador:
    def __init__(self, interfaz):
        self.procesos_nuevos = []
        self.procesos_listos = []
        self.proceso_ejecucion = None
        self.procesos_bloqueados = []
        self.procesos_terminados = []

        self.quantum = 5
        self.reloj_global = 0
        self.total_procesos = 0
        self.max_procesos_memoria = 3

        self.interfaz = interfaz
    
    def __str__(self):
        return "".join(
            str(proceso)+"\n" for proceso in self.procesos_nuevos
        )
    
    def crear_proceso_aleatorio(self):
        operacion = random.choice(['+', '-', '*', '/', '%', '^'])
        dato_operacion_1 = random.randint(0, 100)
        dato_operacion_2 = random.randint(0, 100)
        tiempo_maximo = random.randint(7, 18)

        proceso = Proceso(operacion, dato_operacion_1, dato_operacion_2, tiempo_maximo,self.total_procesos+1)
        proceso.definir_tiempo_llegada(self.reloj_global)
        return proceso
    
    def agregar_proceso(self, proceso):
        self.procesos_nuevos.append(proceso)
        self.total_procesos += 1
        self.interfaz.actualizar_numero_procesos_nuevos(len(self.procesos_nuevos))
        print("A nuevo")

    def agregar_procesos(self, numero_procesos):
        for _ in range(numero_procesos):
            self.agregar_proceso(self.crear_proceso_aleatorio())
    
    def establecer_quantum(self, segundos):
        self.quantum = segundos
        self.interfaz.actualizar_quantum(self.quantum)

    def mover_nuevo_a_listo(self):
        procesos_en_memoria = len(self.procesos_listos) + len(self.procesos_bloqueados) + (1 if self.proceso_ejecucion else 0)
        if self.procesos_nuevos and procesos_en_memoria < self.max_procesos_memoria:
            proceso = self.procesos_nuevos.pop(0)
            self.procesos_listos.append(proceso)
            self.interfaz.actualizar_tabla_procesos_listos(self.procesos_listos)
            
            #self.interfaz.actualizar_numero_procesos_nuevos(len(self.procesos_nuevos))
            print("nuevo a listo")
            return True
        else:
            return False

    def mover_listo_a_ejecucion(self):
        if self.procesos_listos and not self.proceso_ejecucion:
            self.proceso_ejecucion = self.procesos_listos.pop(0)
            self.proceso_ejecucion.definir_tiempo_atendido(self.reloj_global)
            self.interfaz.actualizar_tabla_proceso_en_ejecucion(self.proceso_ejecucion)
            self.interfaz.actualizar_tabla_procesos_listos(self.procesos_listos)
            print("listo a ejecución")
            return True
        else:
            return False
        
    def mover_ejecucion_a_listo(self):
        if self.proceso_ejecucion:
            if self.proceso_ejecucion.tiempo_transcurrido_quantum == self.quantum: 
                self.proceso_ejecucion.reiniciar_tiempo_de_quantum()
                self.procesos_listos.append(self.proceso_ejecucion)
                self.proceso_ejecucion = None
                self.interfaz.actualizar_tabla_procesos_listos(self.procesos_listos)
            return True
        else:
            return False

    def mover_ejecucion_a_terminado(self):
        if self.proceso_ejecucion:
            self.procesos_terminados.append(self.proceso_ejecucion)
            self.proceso_ejecucion = None
            self.interfaz.actualizar_tabla_procesos_terminados(self.procesos_terminados)
            print("ejecucion a terminado")
            return True
        else:
            return False

    def mover_ejecucion_a_bloqueado(self):
        if self.proceso_ejecucion and self.proceso_ejecucion.tiempo_restante > 0:
            self.proceso_ejecucion.reiniciar_tiempo_de_quantum()
            self.procesos_bloqueados.append(self.proceso_ejecucion)
            self.proceso_ejecucion = None
            self.interfaz.actualizar_tabla_procesos_bloqueados(self.procesos_bloqueados)
            self.interfaz.actualizar_tabla_proceso_en_ejecucion(self.proceso_ejecucion)
            print("ejecucion a bloqueado")
            return True
        else:
            return False

    def mover_bloqueado_a_listos(self):
        if self.procesos_bloqueados:
            proceso = self.procesos_bloqueados.pop(0)
            self.procesos_listos.append(proceso)
            self.interfaz.actualizar_tabla_procesos_listos(self.procesos_listos)
            self.interfaz.actualizar_tabla_procesos_bloqueados(self.procesos_bloqueados)
            print("bloqueado a listo")
            return True
        else:
            return False
        
    def actualizar_tiempos_espera(self):
        for proceso in self.procesos_nuevos:
            proceso.actualizar_tiempo_de_espera()

        for proceso in self.procesos_listos:
            proceso.actualizar_tiempo_de_espera()

        for proceso in self.procesos_bloqueados:
            proceso.actualizar_tiempo_de_espera()

    def interrumpir_proceso_entrada_salida(self):
        self.mover_ejecucion_a_bloqueado()
        self.mover_listo_a_ejecucion()
        self.interfaz.reiniciar_tecla_precionada()

    def terminar_proceso_error(self):
        self.proceso_ejecucion.actualizar_error()
        self.proceso_ejecucion.definir_tiempo_finalizacion(self.reloj_global)
        self.mover_ejecucion_a_terminado()
        self.interfaz.reiniciar_tecla_precionada()

    def pausar_proceso(self):
        pass

    def continuar_proceso(self):
        self.interfaz.ui.tabWidget.setCurrentIndex(1)
        self.interfaz.reiniciar_tecla_precionada()

    def agregar_proceso_en_ejecución(self):
        self.agregar_proceso(self.crear_proceso_aleatorio())
        self.mover_nuevo_a_listo()
        self.interfaz.reiniciar_tecla_precionada()

    def mostrar_tabla_bcp(self):
        self.interfaz.mostrar_tabla_bcp()
        time.sleep(2)
        #self.interfaz.reiniciar_tecla_precionada()

    def ejecutar(self):
        while self.mover_nuevo_a_listo():
            pass    
        self.mover_listo_a_ejecucion()
        self.interfaz.actualizar_numero_procesos_nuevos(len(self.procesos_nuevos))
        
        while self.proceso_ejecucion or self.procesos_nuevos or self.procesos_listos or self.procesos_bloqueados:
            while self.proceso_ejecucion and self.proceso_ejecucion.tiempo_transcurrido_quantum < self.quantum:
                if self.interfaz.tecla_precionada == 'e':
                    self.interrumpir_proceso_entrada_salida()
                    break
                elif self.interfaz.tecla_precionada == 'w':
                    self.terminar_proceso_error()
                    break
                elif self.interfaz.tecla_precionada == 'p':
                    self.pausar_proceso()
                elif self.interfaz.tecla_precionada == 'c':
                    self.continuar_proceso()
                elif self.interfaz.tecla_precionada == 'n':
                    self.agregar_proceso_en_ejecución()
                elif self.interfaz.tecla_precionada == 'b':
                    self.mostrar_tabla_bcp()
                else:
                    self.reloj_global += 1

                    if self.proceso_ejecucion:
                        self.proceso_ejecucion.actualizar_tiempo()

                    if self.procesos_bloqueados:
                        for proceso in self.procesos_bloqueados:
                            if proceso.tiempo_bloqueado_restante == 0:
                                proceso.reiniciar_tiempo_de_bloqueo()
                                self.mover_bloqueado_a_listos()

                            else:
                                proceso.actualizar_tiempo_bloqueado()

                    self.actualizar_tiempos_espera()
                    time.sleep(1)
                    
                    if self.proceso_ejecucion:
                        self.interfaz.actualizar_tiempos_proceso(self.proceso_ejecucion)

                        if (self.proceso_ejecucion.tiempo_transcurrido_quantum == self.quantum) and (self.proceso_ejecucion.tiempo_restante != 0):
                            self.mover_ejecucion_a_listo()

                    self.interfaz.actualizar_tabla_procesos_bloqueados(self.procesos_bloqueados)
                    self.interfaz.actualizar_reloj()

                    if self.proceso_ejecucion and self.proceso_ejecucion.tiempo_restante == 0:
                        break              
            
            if self.proceso_ejecucion and self.proceso_ejecucion.tiempo_restante == 0:
                self.proceso_ejecucion.definir_tiempo_finalizacion(self.reloj_global)
                self.mover_ejecucion_a_terminado()
                
            while self.mover_nuevo_a_listo():
                pass
            self.interfaz.actualizar_numero_procesos_nuevos(len(self.procesos_nuevos))
            self.mover_listo_a_ejecucion()

            if not self.proceso_ejecucion and self.procesos_bloqueados:
                for proceso in self.procesos_bloqueados:
                    if proceso.tiempo_bloqueado_restante == 0:
                        proceso.reiniciar_tiempo_de_bloqueo()
                        self.mover_bloqueado_a_listos()
                    else:
                        proceso.actualizar_tiempo_bloqueado()
                
                self.reloj_global += 1
                time.sleep(1)

                self.interfaz.actualizar_tabla_procesos_bloqueados(self.procesos_bloqueados)
                self.interfaz.actualizar_reloj()

        self.interfaz.actualizar_tabla_resultados(self.procesos_terminados)