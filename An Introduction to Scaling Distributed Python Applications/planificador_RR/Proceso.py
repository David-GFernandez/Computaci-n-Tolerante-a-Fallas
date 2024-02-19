class Proceso:
    def __init__(self, operacion, dato_operacion_1, dato_operacion_2, tiempo_maximo, numero_programa):
        self.numero_programa = numero_programa
        self.operacion = operacion
        self.dato_operacion_1 = dato_operacion_1
        self.dato_operacion_2 = dato_operacion_2

        self.tiempo_maximo = tiempo_maximo
        self.tiempo_restante = self.tiempo_maximo
        self.tiempo_transcurrido = 0
        
        self.tiempo_de_bloqueo = 9
        self.tiempo_llegada = 0
        self.tiempo_finalizacion = 0
        self.tiempo_atendido = 0
        self.tiempo_espera = 0
        self.tiempo_bloqueado_restante = self.tiempo_de_bloqueo
        self.tiempo_bloqueado = 0
        self.tiempo_transcurrido_quantum = 0

        self.error = False

    def __str__(self):
        return(
            "Numero de Programa: " + str(self.numero_programa) + "\n" +
            "Operación: " + str(self.dato_operacion_1) + " " + self.operacion + " " + str(self.dato_operacion_2) +"\n" +
            "Tiempo Maximo Estimado: " + str(self.tiempo_maximo) + "\n" +
            "------------------------------------"
        )
    
    def definir_tiempo_llegada(self,tiempo):
        self.tiempo_llegada = tiempo

    def definir_tiempo_finalizacion(self,tiempo):
        self.tiempo_finalizacion = tiempo

    def definir_tiempo_atendido(self,tiempo):
        self.tiempo_atendido = tiempo
    
    def validar_operacion(self):
        operaciones_validas = ['+', '-', '*', '/', '%', '^']
        return self.operacion in operaciones_validas

    def validar_tiempo_maximo(self):
        return self.tiempo_maximo > 0
    
    def actualizar_tiempo(self):
        self.tiempo_transcurrido += 1
        self.tiempo_transcurrido_quantum += 1
        self.tiempo_restante -= 1

    def actualizar_tiempo_bloqueado(self):
        self.tiempo_bloqueado += 1
        self.tiempo_bloqueado_restante -= 1

    def actualizar_tiempo_de_espera(self):
        self.tiempo_espera += 1
    
    def reiniciar_tiempo_de_bloqueo(self):
        self.tiempo_bloqueado_restante = self.tiempo_de_bloqueo

    def reiniciar_tiempo_de_quantum(self):
        self.tiempo_transcurrido_quantum = 0

    def actualizar_error(self):
        self.error = not self.error

    def realizar_operacion(self):
        if not self.validar_operacion():
            return None
        
        if self.operacion == '+':
            return self.dato_operacion_1 + self.dato_operacion_2
        elif self.operacion == '-':
            return self.dato_operacion_1 - self.dato_operacion_2
        elif self.operacion == '*':
            return self.dato_operacion_1 * self.dato_operacion_2
        elif self.operacion == '/':
            if self.dato_operacion_2 != 0:
                return self.dato_operacion_1 / self.dato_operacion_2
            else:
                self.error = True
                return None
        elif self.operacion == '%':
            if self.dato_operacion_2 != 0:
                return self.dato_operacion_1 % self.dato_operacion_2
            else:
                self.error = True
                return None
        elif self.operacion == '^':
            return self.dato_operacion_1 ** self.dato_operacion_2

    def obtener_tiempo_retorno(self):
        return self.tiempo_finalizacion - self.tiempo_llegada

    def obtener_tiempo_respuesta(self):
        if self.numero_programa != 1 and self.tiempo_atendido == 0:
            return -1
        else:
            return self.tiempo_atendido - self.tiempo_llegada
    
    def obtener_tiempo_espera(self):
        return self.tiempo_espera

    def obtener_tiempo_servicio(self):
        return self.tiempo_maximo - self.tiempo_restante   