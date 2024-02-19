from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Slot

from mainwindow import Ui_MainWindow

from Planificador import Planificador

from Threadering import SimulacionThread
from Threadering import TecladoThread

class Interfaz(QMainWindow):
    def __init__(self):
        super(Interfaz, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.planificador = Planificador(self)
        self.tecla_precionada = None

        self.simulacion_thread = None
        self.teclado_thread = None

        self.ui.tableWidget_procesosBloqueados.verticalHeader().setVisible(False)
        self.ui.tableWidget_procesosListos.verticalHeader().setVisible(False)
        self.ui.tableWidget_procesoEjecucion.horizontalHeader().setVisible(False)
        self.ui.tableWidget_procesosTerminados.verticalHeader().setVisible(False)
        self.ui.tableWidget_resultados.horizontalHeader().setVisible(False)
        self.ui.tableWidget_bcp.horizontalHeader().setVisible(False)

        self.ui.pushButton_iniciar.clicked.connect(self.iniciar)
        self.ui.pushButton_agregarProcesos.clicked.connect(self.agregar_procesos)
        self.ui.pushButton_iniciar.clicked.connect(self.iniciar)
        self.ui.pushButton_establecerQuantum.clicked.connect(self.establecer_quantum)
    
    def dar_formato_tiempo(self,tiempo):
        minutos = tiempo // 60
        segundos = tiempo % 60
        return str(minutos) + ":" + str(segundos)

    def limpiar_entradas_datos(self):
        self.ui.spinBox_numeroProcesos.clear()

    def actualizar_texto_lista_de_procesos(self):
        self.ui.plainTextEdit_listaProcesos.clear()
        self.ui.plainTextEdit_listaProcesos.insertPlainText(str(self.planificador))

    def actualizar_numero_procesos_nuevos(self, numero_procesos_nuevos):
        self.ui.lineEdit_procesosNuevos.setText(str(numero_procesos_nuevos))

    def actualizar_quantum(self,quantum):
        self.ui.lineEdit_valorQuantum.setText(str(quantum))
    
    def actualizar_tabla_procesos_bloqueados(self, lista):
        self.ui.tableWidget_procesosBloqueados.setRowCount(len(lista))

        for row, proceso in enumerate(lista):
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            tiempo_bloqueado = QTableWidgetItem(str(proceso.tiempo_bloqueado))

            self.ui.tableWidget_procesosBloqueados.setItem(row, 0, numero_programa_item)
            self.ui.tableWidget_procesosBloqueados.setItem(row, 1, tiempo_bloqueado)
    
    def actualizar_tabla_procesos_listos(self, lista):
        self.ui.tableWidget_procesosListos.setRowCount(len(lista))

        for row, proceso in enumerate(lista):
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            tiempo_estimado_item = QTableWidgetItem(str(proceso.tiempo_maximo))
            tiempo_restante_item = QTableWidgetItem(str(proceso.tiempo_restante))

            self.ui.tableWidget_procesosListos.setItem(row, 0, numero_programa_item)
            self.ui.tableWidget_procesosListos.setItem(row, 1, tiempo_estimado_item)
            self.ui.tableWidget_procesosListos.setItem(row, 2, tiempo_restante_item)

    def actualizar_tabla_proceso_en_ejecucion(self, proceso):
        if proceso:
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            operacion_item = QTableWidgetItem(proceso.operacion)
            tiempo_estimado_item = QTableWidgetItem(str(proceso.tiempo_maximo))
            tiempo_transcurrido_item = QTableWidgetItem(str(proceso.tiempo_transcurrido))
            tiempo_restante_item = QTableWidgetItem(str(proceso.tiempo_restante))
            quantum_item = QTableWidgetItem(str(proceso.tiempo_transcurrido_quantum))
        else:
            numero_programa_item = QTableWidgetItem("")
            operacion_item = QTableWidgetItem("")
            tiempo_estimado_item = QTableWidgetItem("")
            tiempo_transcurrido_item = QTableWidgetItem("")
            tiempo_restante_item = QTableWidgetItem("")
            quantum_item = QTableWidgetItem("")

        self.ui.tableWidget_procesoEjecucion.setItem(0, 0, numero_programa_item)
        self.ui.tableWidget_procesoEjecucion.setItem(1, 0, operacion_item)
        self.ui.tableWidget_procesoEjecucion.setItem(2, 0, tiempo_estimado_item)
        self.ui.tableWidget_procesoEjecucion.setItem(3, 0, tiempo_transcurrido_item)
        self.ui.tableWidget_procesoEjecucion.setItem(4, 0, tiempo_restante_item)
        self.ui.tableWidget_procesoEjecucion.setItem(5, 0, quantum_item)
        

    def actualizar_tabla_procesos_terminados(self,lista):
        self.ui.tableWidget_procesosTerminados.setRowCount(len(lista))

        for row, proceso in enumerate(lista):
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            dato_operacion_1_item = QTableWidgetItem(str(proceso.dato_operacion_1))
            operacion_item = QTableWidgetItem(proceso.operacion)
            dato_operacion_2_item = QTableWidgetItem(str(proceso.dato_operacion_2))
            if proceso.error:
                resultado_item = QTableWidgetItem("Error")
            else:
                resultado_item = QTableWidgetItem(str(proceso.realizar_operacion()))

            self.ui.tableWidget_procesosTerminados.setItem(row, 0, numero_programa_item)
            self.ui.tableWidget_procesosTerminados.setItem(row, 1, dato_operacion_1_item)
            self.ui.tableWidget_procesosTerminados.setItem(row, 2, operacion_item)
            self.ui.tableWidget_procesosTerminados.setItem(row, 3, dato_operacion_2_item)
            self.ui.tableWidget_procesosTerminados.setItem(row, 4, resultado_item)

    def actualizar_tabla_resultados(self,lista):
        self.ui.tableWidget_resultados.setColumnCount(len(lista))

        for column, proceso in enumerate(lista):
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            dato_operacion_1_item = QTableWidgetItem(str(proceso.dato_operacion_1))
            operacion_item = QTableWidgetItem(proceso.operacion)
            dato_operacion_2_item = QTableWidgetItem(str(proceso.dato_operacion_2))
            if proceso.error:
                resultado_item = QTableWidgetItem("Error")
            else:
                resultado_item = QTableWidgetItem(str(proceso.realizar_operacion()))
            
            tiempo_maximo_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_maximo))
            tiempo_llegada_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_llegada))
            tiempo_finalizacion_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_finalizacion))
            tiempo_retorno_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_retorno())) 
            tiempo_respuesta_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_respuesta()))
            tiempo_espera_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_espera()))
            tiempo_servicio_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_servicio()))

            self.ui.tableWidget_resultados.setItem(0, column, numero_programa_item)
            self.ui.tableWidget_resultados.setItem(1, column, dato_operacion_1_item)
            self.ui.tableWidget_resultados.setItem(2, column, operacion_item)
            self.ui.tableWidget_resultados.setItem(3, column, dato_operacion_2_item)
            self.ui.tableWidget_resultados.setItem(4, column, resultado_item)
            self.ui.tableWidget_resultados.setItem(5, column, tiempo_maximo_item)
            self.ui.tableWidget_resultados.setItem(6, column, tiempo_llegada_item)
            self.ui.tableWidget_resultados.setItem(7, column, tiempo_finalizacion_item)
            self.ui.tableWidget_resultados.setItem(8, column, tiempo_retorno_item)
            self.ui.tableWidget_resultados.setItem(9, column, tiempo_respuesta_item)
            self.ui.tableWidget_resultados.setItem(10, column, tiempo_espera_item)
            self.ui.tableWidget_resultados.setItem(11, column, tiempo_servicio_item)

    def actualizar_reloj(self):
        segundos = self.planificador.reloj_global
        minutos = segundos // 60
        segundos = segundos % 60
        self.ui.lcdNumber.display(f"{minutos:02d}:{segundos:02d}")

    def actualizar_tiempos_proceso(self, proceso):
        tiempo_transcurrido_item = QTableWidgetItem(str(proceso.tiempo_transcurrido))
        tiempo_restante_item = QTableWidgetItem(str(proceso.tiempo_restante))
        quantum_item = QTableWidgetItem(str(proceso.tiempo_transcurrido_quantum))

        self.ui.tableWidget_procesoEjecucion.setItem(3, 0, tiempo_transcurrido_item)
        self.ui.tableWidget_procesoEjecucion.setItem(4, 0, tiempo_restante_item)
        self.ui.tableWidget_procesoEjecucion.setItem(5, 0, quantum_item)

    def mostrar_tabla_bcp(self):
        i = 0
    
        self.ui.tableWidget_bcp.setColumnCount(self.planificador.total_procesos)

        for proceso in self.planificador.procesos_nuevos:
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            estado_item = QTableWidgetItem("Nuevo")

            self.ui.tableWidget_bcp.setItem(0, i, numero_programa_item)
            self.ui.tableWidget_bcp.setItem(1, i, estado_item)

            i += 1

        for proceso in self.planificador.procesos_listos:
            tiempo_respuesta = proceso.obtener_tiempo_respuesta()
            
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            estado_item = QTableWidgetItem("Listo")
            dato_operacion_1_item = QTableWidgetItem(str(proceso.dato_operacion_1))
            operacion_item = QTableWidgetItem(proceso.operacion)
            dato_operacion_2_item = QTableWidgetItem(str(proceso.dato_operacion_2))
            tiempo_llegada_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_llegada))
            tiempo_espera_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_espera()))
            tiempo_servicio_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_servicio()))
            tiempo_restante_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_restante))
            if tiempo_respuesta >= 0:
                tiempo_respuesta_item = QTableWidgetItem(self.dar_formato_tiempo(tiempo_respuesta))
            else:
                tiempo_respuesta_item = QTableWidgetItem("")

            self.ui.tableWidget_bcp.setItem(0, i, numero_programa_item)
            self.ui.tableWidget_bcp.setItem(1, i, estado_item)
            self.ui.tableWidget_bcp.setItem(2, i, dato_operacion_1_item)
            self.ui.tableWidget_bcp.setItem(3, i, operacion_item)
            self.ui.tableWidget_bcp.setItem(4, i, dato_operacion_2_item)
            self.ui.tableWidget_bcp.setItem(6, i, tiempo_llegada_item)
            self.ui.tableWidget_bcp.setItem(9, i, tiempo_espera_item)
            self.ui.tableWidget_bcp.setItem(10, i, tiempo_servicio_item)
            self.ui.tableWidget_bcp.setItem(11, i, tiempo_restante_item)
            self.ui.tableWidget_bcp.setItem(12, i, tiempo_respuesta_item)

            i += 1

        if self.planificador.proceso_ejecucion:
            proceso_ejecucion = self.planificador.proceso_ejecucion
            numero_programa_item = QTableWidgetItem(str(proceso_ejecucion.numero_programa))
            estado_item = QTableWidgetItem("Ejecución")
            dato_operacion_1_item = QTableWidgetItem(str(proceso_ejecucion.dato_operacion_1))
            operacion_item = QTableWidgetItem(proceso_ejecucion.operacion)
            dato_operacion_2_item = QTableWidgetItem(str(proceso_ejecucion.dato_operacion_2))
            tiempo_llegada_item = QTableWidgetItem(self.dar_formato_tiempo(proceso_ejecucion.tiempo_llegada))
            tiempo_espera_item = QTableWidgetItem(self.dar_formato_tiempo(proceso_ejecucion.obtener_tiempo_espera()))
            tiempo_servicio_item = QTableWidgetItem(self.dar_formato_tiempo(proceso_ejecucion.obtener_tiempo_servicio()))
            tiempo_restante_item = QTableWidgetItem(self.dar_formato_tiempo(proceso_ejecucion.tiempo_restante))
            tiempo_respuesta_item = QTableWidgetItem(self.dar_formato_tiempo(proceso_ejecucion.obtener_tiempo_respuesta()))

            self.ui.tableWidget_bcp.setItem(0, i, numero_programa_item)
            self.ui.tableWidget_bcp.setItem(1, i, estado_item)
            self.ui.tableWidget_bcp.setItem(2, i, dato_operacion_1_item)
            self.ui.tableWidget_bcp.setItem(3, i, operacion_item)
            self.ui.tableWidget_bcp.setItem(4, i, dato_operacion_2_item)
            self.ui.tableWidget_bcp.setItem(6, i, tiempo_llegada_item)
            self.ui.tableWidget_bcp.setItem(9, i, tiempo_espera_item)
            self.ui.tableWidget_bcp.setItem(10, i, tiempo_servicio_item)
            self.ui.tableWidget_bcp.setItem(11, i, tiempo_restante_item)
            self.ui.tableWidget_bcp.setItem(12, i, tiempo_respuesta_item)

            i += 1

        for proceso in self.planificador.procesos_bloqueados:
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            estado_item = QTableWidgetItem("Bloqueado")
            dato_operacion_1_item = QTableWidgetItem(str(proceso.dato_operacion_1))
            operacion_item = QTableWidgetItem(proceso.operacion)
            dato_operacion_2_item = QTableWidgetItem(str(proceso.dato_operacion_2))
            tiempo_llegada_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_llegada))
            tiempo_espera_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_espera()))
            tiempo_servicio_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_servicio()))
            tiempo_restante_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_restante))
            tiempo_respuesta_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_respuesta()))

            self.ui.tableWidget_bcp.setItem(0, i, numero_programa_item)
            self.ui.tableWidget_bcp.setItem(1, i, estado_item)
            self.ui.tableWidget_bcp.setItem(2, i, dato_operacion_1_item)
            self.ui.tableWidget_bcp.setItem(3, i, operacion_item)
            self.ui.tableWidget_bcp.setItem(4, i, dato_operacion_2_item)
            self.ui.tableWidget_bcp.setItem(6, i, tiempo_llegada_item)
            self.ui.tableWidget_bcp.setItem(9, i, tiempo_espera_item)
            self.ui.tableWidget_bcp.setItem(10, i, tiempo_servicio_item)
            self.ui.tableWidget_bcp.setItem(11, i, tiempo_restante_item)
            self.ui.tableWidget_bcp.setItem(12, i, tiempo_respuesta_item)

            i += 1

        for proceso in self.planificador.procesos_terminados:
            numero_programa_item = QTableWidgetItem(str(proceso.numero_programa))
            estado_item = QTableWidgetItem("Terminado")
            dato_operacion_1_item = QTableWidgetItem(str(proceso.dato_operacion_1))
            operacion_item = QTableWidgetItem(proceso.operacion)
            dato_operacion_2_item = QTableWidgetItem(str(proceso.dato_operacion_2))
            if proceso.error:
                resultado_item = QTableWidgetItem("Error")
            else:
                resultado_item = QTableWidgetItem(str(proceso.realizar_operacion()))
            tiempo_llegada_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_llegada))
            tiempo_finalizacion_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_finalizacion))
            tiempo_retorno_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_retorno()))
            tiempo_espera_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_espera()))
            tiempo_servicio_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_servicio()))
            tiempo_restante_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.tiempo_restante))
            tiempo_respuesta_item = QTableWidgetItem(self.dar_formato_tiempo(proceso.obtener_tiempo_respuesta()))

            self.ui.tableWidget_bcp.setItem(0, i, numero_programa_item)
            self.ui.tableWidget_bcp.setItem(1, i, estado_item)
            self.ui.tableWidget_bcp.setItem(2, i, dato_operacion_1_item)
            self.ui.tableWidget_bcp.setItem(3, i, operacion_item)
            self.ui.tableWidget_bcp.setItem(4, i, dato_operacion_2_item)
            self.ui.tableWidget_bcp.setItem(5, i, resultado_item)
            self.ui.tableWidget_bcp.setItem(6, i, tiempo_llegada_item)
            self.ui.tableWidget_bcp.setItem(7, i, tiempo_finalizacion_item)
            self.ui.tableWidget_bcp.setItem(8, i, tiempo_retorno_item)
            self.ui.tableWidget_bcp.setItem(9, i, tiempo_espera_item)
            self.ui.tableWidget_bcp.setItem(10, i, tiempo_servicio_item)
            self.ui.tableWidget_bcp.setItem(11, i, tiempo_restante_item)
            self.ui.tableWidget_bcp.setItem(12, i, tiempo_respuesta_item)

            i += 1 

        self.ui.tabWidget.setCurrentIndex(2)

    def simulacion_finalizada(self):
        self.teclado_thread.detener()
        QMessageBox.information(self, "Simulación Terminada", "La simulación ha terminado.")

    def actualizar_tecla_presionada(self, tecla):
        self.tecla_precionada = tecla
    
    def reiniciar_tecla_precionada(self):
        self.tecla_precionada = None

    @Slot()
    def agregar_procesos(self):
        self.planificador.agregar_procesos(self.ui.spinBox_numeroProcesos.value())
        self.actualizar_texto_lista_de_procesos()
        self.limpiar_entradas_datos()

    @Slot()
    def establecer_quantum(self):
        self.planificador.establecer_quantum(self.ui.spinBox_Quantum.value())
        
    @Slot()
    def iniciar(self):
        if not self.simulacion_thread or not self.simulacion_thread.isRunning():
            self.simulacion_thread = SimulacionThread(self.planificador)
            self.simulacion_thread.finalizada.connect(self.simulacion_finalizada)
            self.simulacion_thread.start()
            
        if not self.teclado_thread or not self.teclado_thread.isRunning():
            self.teclado_thread = TecladoThread()
            self.teclado_thread.tecla_presionada.connect(self.actualizar_tecla_presionada)
            self.teclado_thread.start()