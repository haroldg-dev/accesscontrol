import sys
import time
import datetime
import os
import pyodbc
import socket
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import requests
import json
from requests.structures import CaseInsensitiveDict

# sudo date 06230643
# Definimos aplicacion
app = QApplication(sys.argv)
app.setStyle("FUsion")
# Variables globales
usr = "usrPi"
iIdSede = []
vcCodigoSede = []
vcDescripcion = []
iIdEstado = []
vcSegmentoRedInferior = []
vcSegmentoRedSuperior = []
iAforo = []
global_text = ""
win2 = False

# Consulta hora al servidor


def sqlgetdate():
    a = False
    try:
        conn = pyodbc.connect('DRIVER={FreeTDS};'
                              'Server=172.16.1.33;'
                              'PORT=1433;'
                              'DATABASE=CITAS_CHAMAN_20130930;'
                              'UID=usrRPI;'
                              'PWD=/elexit0;'
                              'TDS_Version=7.4')
        cursor = conn.cursor()
        comand = "SELECT GETDATE()"
        # print(comand)
        cursor.execute(comand)
        results = cursor.fetchone()
        # print(results)
        while results:
            fecha = str(results[0])
            writedate(fecha)
            a = True
            results = cursor.fetchone()
            conn.commit()
        return a
    except (Exception, pyodbc.DatabaseError) as error:
        print(error)
        a = False
        return a
    return a
# SETEO DE HORA


def writedate(date):
    fecha = date[0:10]
    hora = date[11:19]
    fx = fecha.split("-")
    hx = hora.split(':')
    print(fecha)
    print(hora)
    cmd = "sudo date -s '" + fecha + " " + hora + "'"
    # sudo date 06230643
    # sudo date -s + f1-f2-f3 " " +h1+h2+h3
    os.system(cmd)
    # os.system("sudo date 06250830")
    print(cmd)


class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)

        self.txtDNI = QLineEdit(self)
        self.txtDNI.setPlaceholderText("Ingrese DNI")
        self.txtDNI.setGeometry(200, 200, 100, 30)
        self.txtDNI.returnPressed.connect(self.onPressed)

        self.fondo1 = QLabel(self)
        self.fondo1.setGeometry(-1, 0, 490, 800)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/fondoo022.jpg')
        self.fondo1.setPixmap(pixmap)
        self.fondo1.setHidden(False)

        self.fondo2 = QLabel(self)
        self.fondo2.setGeometry(-1, 0, 510, 800)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/fondoo011.jpg')
        self.fondo2.setPixmap(pixmap)
        self.fondo2.setHidden(True)

        self.fondorrhh = QLabel(self)
        self.fondorrhh.setGeometry(-1, 0, 490, 800)
        pixmap = QPixmap(
            '/home/pi/PANELNATCLAR/recursos/images2/fondorrhh.jpg')
        pixmap = pixmap.scaledToWidth(480)
        self.fondorrhh.setPixmap(pixmap)
        self.fondorrhh.setHidden(True)

        """self.silueta = QLabel(self)
        self.silueta.setGeometry(0, 0, 480, 700)
        pixmap = QPixmap('D:/cabinatermica/recursos/images/silueta.png')
        # pixmap = pixmap.scaledToWidth(500)
        self.silueta.setPixmap(pixmap)
        self.silueta.move(-10, -30)
        self.silueta.setHidden(False)"""

        self.recrojo = QLabel(self)
        self.recrojo.setGeometry(0, 0, 480, 200)  # (ancho,alto)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/recrojo.jpg')
        pixmap = pixmap.scaledToWidth(480)
        self.recrojo.setPixmap(pixmap)
        self.recrojo.move(0, 400)
        self.recrojo.setHidden(True)

        self.gracias = QLabel(self)
        self.gracias.setGeometry(0, 0, 480, 200)  # (ancho,alto)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/gracias.jpg')
        # pixmap = pixmap.scaledToWidth(440)
        self.gracias.setPixmap(pixmap)
        self.gracias.move(15, 450)
        self.gracias.setHidden(True)

        self.nosede = QLabel(self)
        self.nosede.setFont(QFont("Arial", 14, QFont.Black))
        self.nosede.setGeometry(0, 0, 480, 30)
        self.nosede.setStyleSheet("color : rgb(255,255,255)")
        self.nosede.setText("SU CITA ES EN:")  # change label text
        self.nosede.move(40, 490)
        self.nosede.setHidden(True)

        self.lblestado = QLabel(self)
        self.lblestado.setFont(QFont("Arial", 14, QFont.Black))
        self.lblestado.setGeometry(0, 0, 480, 30)
        self.lblestado.setStyleSheet("color : rgb(255,255,255)")
        self.lblestado.setText(
            "CITA EN REVISION MESA DE AYUDA")  # change label text
        self.lblestado.move(50, 485)
        self.lblestado.setHidden(True)

        self.lblsedecita = QLabel(self)
        self.lblsedecita.setFont(QFont("Arial", 14, QFont.Black))
        self.lblsedecita.setGeometry(0, 0, 480, 30)
        self.lblsedecita.setStyleSheet("color : rgb(255,255,255)")
        self.lblsedecita.setText("")  # change label text
        self.lblsedecita.move(210, 490)
        self.lblsedecita.setHidden(True)

        self.nocita = QLabel(self)
        self.nocita.setGeometry(0, 0, 480, 200)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/nocita.png')
        pixmap = pixmap.scaledToWidth(480)
        self.nocita.setPixmap(pixmap)
        self.nocita.move(0, 400)
        self.nocita.setHidden(True)

        self.lbladmitido = QLabel(self)
        self.lbladmitido.setFont(QFont("Arial", 18, QFont.Black))
        self.lbladmitido.setGeometry(0, 0, 400, 400)
        self.lbladmitido.setStyleSheet("color : rgb(255,255,255)")
        self.lbladmitido.setText("ADMITIDO")  # change label text
        self.lbladmitido.move(150, 330)
        self.lbladmitido.setHidden(True)

        self.lblGlobal = QLabel(self)
        self.lblGlobal.setFont(QFont("Arial Black", 12, QFont.Black))
        self.lblGlobal.setGeometry(0, 0, 120, 50)
        self.lblGlobal.setStyleSheet("color : rgb(242,126,37)")
        self.lblGlobal.setText("0")  # change label text
        self.lblGlobal.move(325, 170)
        self.lblGlobal.setHidden(False)

        self.lblfecha = QLabel(self)
        self.lblfecha.setFont(QFont("Arial Black", 10, QFont.Black))
        self.lblfecha.setGeometry(0, 0, 140, 50)
        self.lblfecha.setStyleSheet("color : rgb(34,33,74)")
        self.lblfecha.setText("")  # change label text
        self.lblfecha.move(335, 15)
        self.lblfecha.setHidden(False)

        self.lblhora = QLabel(self)
        self.lblhora.setFont(QFont("Arial Black", 10, QFont.Black))
        self.lblhora.setGeometry(0, 0, 100, 50)
        self.lblhora.setStyleSheet("color : rgb(34,33,74)")
        self.lblhora.setText("")  # change label text
        self.lblhora.move(376, 32)
        self.lblhora.setHidden(False)

        self.lblsede = QLabel(self)
        self.lblsede.setFont(QFont("Arial", 10, QFont.Black))
        self.lblsede.setGeometry(0, 0, 120, 50)
        self.lblsede.setStyleSheet("color : rgb(255,255,255)")
        self.lblsede.setText("La Victoria")  # change label text
        self.lblsede.move(360, 748)
        self.lblsede.setHidden(False)

        self.lblAmax = QLabel(self)
        self.lblAmax.setFont(QFont("Arial", 12, QFont.Black))
        self.lblAmax.setGeometry(0, 0, 120, 30)
        self.lblAmax.setStyleSheet("color : rgb(34,33,74)")
        self.lblAmax.setText("")  # change label text
        self.lblAmax.move(390, 150)
        self.lblAmax.setHidden(False)

        self.lblAreal = QLabel(self)
        self.lblAreal.setFont(QFont("Arial", 12, QFont.Black))
        self.lblAreal.setGeometry(0, 0, 120, 30)
        self.lblAreal.setStyleSheet("color : rgb(34,33,74)")
        self.lblAreal.setText("")  # change label text
        self.lblAreal.move(325, 150)
        self.lblAreal.setHidden(False)

        self.lblAmaxArea = QLabel(self)
        self.lblAmaxArea.setFont(QFont("Arial", 12, QFont.Black))
        self.lblAmaxArea.setGeometry(0, 0, 120, 30)
        self.lblAmaxArea.setStyleSheet("color : rgb(34,33,74)")
        self.lblAmaxArea.setText("")  # change label text
        self.lblAmaxArea.move(390, 120)
        self.lblAmaxArea.setHidden(False)

        self.lblArealArea = QLabel(self)
        self.lblArealArea.setFont(QFont("Arial", 12, QFont.Black))
        self.lblArealArea.setGeometry(0, 0, 120, 30)
        self.lblArealArea.setStyleSheet("color : rgb(34,33,74)")
        self.lblArealArea.setText("")  # change label text
        self.lblArealArea.move(325, 120)
        self.lblArealArea.setHidden(False)

        self.lblDNI = QLabel(self)
        self.lblDNI.setFont(QFont("Arial", 14, QFont.Black))
        self.lblDNI.setGeometry(0, 0, 140, 30)
        self.lblDNI.setStyleSheet("color : rgb(242,126,37)")
        self.lblDNI.setText("76547319")  # change label text
        self.lblDNI.move(62, 330)
        self.lblDNI.setHidden(True)

        self.lblNombre = QLabel(self)
        self.lblNombre.setFont(QFont("Arial", 14, QFont.Bold))
        self.lblNombre.setGeometry(0, 0, 400, 30)
        self.lblNombre.setStyleSheet("color : rgb(242,126,37)")
        self.lblNombre.setText("HAROLD")  # change label text
        self.lblNombre.move(62, 420)
        self.lblNombre.setHidden(True)

        self.lblEmpresa = QLabel(self)
        self.lblEmpresa.setFont(QFont("Arial", 14, QFont.Bold))
        self.lblEmpresa.setGeometry(0, 0, 400, 30)
        self.lblEmpresa.setStyleSheet("color : rgb(242,126,37)")
        self.lblEmpresa.setText("NATCLAR")  # change label text
        self.lblEmpresa.move(62, 505)
        self.lblEmpresa.setHidden(True)

        self.lbllocal = QLabel(self)
        self.lbllocal.setFont(QFont("Arial", 14, QFont.Black))
        self.lbllocal.setGeometry(0, 0, 300, 30)
        self.lbllocal.setStyleSheet("color : rgb(242,126,37)")
        self.lbllocal.setText("SURCO")  # change label text
        self.lbllocal.move(62, 590)
        self.lbllocal.setHidden(True)

        self.lblcita = QLabel(self)
        self.lblcita.setFont(QFont("Arial", 14, QFont.Black))
        self.lblcita.setGeometry(0, 0, 140, 30)
        self.lblcita.setStyleSheet("color : rgb(242,126,37)")
        self.lblcita.setText("7:00")  # change label text
        self.lblcita.move(62, 670)
        self.lblcita.setHidden(True)

        self.welcome = QLabel(self)
        self.welcome.setGeometry(0, 0, 480, 100)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/welcome.jpg')
        pixmap = pixmap.scaledToWidth(480)
        self.welcome.setPixmap(pixmap)
        self.welcome.move(0, 725)
        self.welcome.setHidden(True)

        self.filtroon = QLabel(self)
        self.filtroon.setGeometry(0, 0, 480, 100)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/filtroon.jpg')
        pixmap = pixmap.scaledToWidth(480)
        self.filtroon.setPixmap(pixmap)
        self.filtroon.move(0, 725)
        self.filtroon.setHidden(True)

        self.filtrooff = QLabel(self)
        self.filtrooff.setGeometry(0, 0, 480, 100)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images/filtrooff.jpg')
        pixmap = pixmap.scaledToWidth(480)
        self.filtrooff.setPixmap(pixmap)
        self.filtrooff.move(0, 725)
        self.filtrooff.setHidden(True)

        self.rrhhtrue = QLabel(self)
        self.rrhhtrue.setGeometry(0, 0, 480, 100)
        pixmap = QPixmap('/home/pi/PANELNATCLAR/recursos/images2/rrhhtrue.png')
        pixmap = pixmap.scaledToWidth(480)
        self.rrhhtrue.setPixmap(pixmap)
        self.rrhhtrue.move(0, 725)
        self.rrhhtrue.setHidden(True)

        self.rrhhFalse = QLabel(self)
        self.rrhhFalse.setGeometry(0, 0, 480, 100)
        pixmap = QPixmap(
            '/home/pi/PANELNATCLAR/recursos/images2/rrhhfalse.png')
        pixmap = pixmap.scaledToWidth(480)
        self.rrhhFalse.setPixmap(pixmap)
        self.rrhhFalse.move(0, 725)
        self.rrhhFalse.setHidden(True)

        self.DNI = ""

    def onPressed(self):
        self.DNI = self.txtDNI.text()
        print(len(self.DNI))
        # ACTUALIZACION 27/07/20
        if len(self.DNI) == 8:
            print("DNI CORRECTO")
            print(self.DNI)
            self.txtDNI.setText("")
            self.lblDNI.setText(self.DNI)
        else:
            print("DNI ERRONEO")
            self.txtDNI.setText("")
            self.DNI = "ERRONEO"

        # self.fondo1.setHidden(True)
        # self.fondo2.setHidden(False)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.title = "CONTROL DE ACCESO"
        self.top = 0
        self.left = 0
        self.width = 480
        self.height = 800
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.central = QWidget(self)
        self.central.setContentsMargins(0, 0, 0, 0)
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.displays = QHBoxLayout()
        self.display = ImageWidget(self)
        self.displays.addWidget(self.display)
        self.vlayout.addLayout(self.displays)
        self.central.setLayout(self.vlayout)
        self.setCentralWidget(self.central)

        buttonWindow1 = QPushButton('X', self)
        buttonWindow1.setGeometry(0, 0, 50, 30)
        buttonWindow1.move(428, 0)
        buttonWindow1.setStyleSheet("background-color:rgb(204,204,204)")
        buttonWindow1.clicked.connect(self.close)

        self.btn01 = QPushButton('', self)
        self.btn01.setGeometry(0, 0, 70, 70)
        self.btn01.move(53, 130)
        self.btn01.clicked.connect(self.btn01_onClick)
        self.btn01.setIcon(
            QIcon("/home/pi/PANELNATCLAR/recursos/images/bnt1.png"))
        self.btn01.setIconSize((QSize(70, 70)))
        self.btn01.setStyleSheet("border : none")

        self.btnnatclar = QPushButton('', self)
        self.btnnatclar.setGeometry(0, 0, 100, 100)
        self.btnnatclar.move(31, 2)
        self.btnnatclar.clicked.connect(self.btnnatclar_onClick)
        self.btnnatclar.setIcon(
            QIcon("/home/pi/PANELNATCLAR/recursos/images2/natclaron.jpg"))
        self.btnnatclar.setIconSize((QSize(95, 90)))
        self.btnnatclar.setStyleSheet("border : none")

        # VARIABLES DEL LOGICA DE PROGRAMA
        self.alwaysfalse = False
        self.time1 = datetime.datetime.now()
        self.segundos = ""
        self.clock5s = False
        self.int = 0
        self.int1 = 0
        self.reset = False
        self.DIA = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        print(self.DIA)
        self.iIdSede = [None] * 3
        self.sede = [None] * 3
        self.sedecodigo = [None] * 3
        self.consult = False
        self.servidorok = False
        self.writemensaje = False
        self.full = False
        self.mensaje = ""
        self.vip = False
        self.enablefiltro = False
        self.sayfiltro = False
        self.timeoff = None

        self.rrhh = False
        self.sayrrhh = False

        # TABLA IP SEDE
        self.vcCodigoSede = [""]
        self.vcDescripcion = [""]
        self.iIdEstado = [""]
        self.vcSegmentoRedInferior = [""]
        self.vcSegmentoRedSuperior = [""]
        self.iAforo = [None] * 3
        self.AforoArea = 0
        self.AforoActuralArea = 0
        # TABLA CITA
        self.vcNombres = [None]  # NOMBRES
        self.vcApellidoPaterno = [None]  # APE_PATERNO
        self.vcApellidoMaterno = [None]  # APE_MATERNO
        self.vcCodigoSede = [None]
        self.vcSede = [None]  # centro
        self.vcEstado = [None]
        self.vcCompania = [None]  # DES_COMPANIA
        self.vcUnidad = [None]  # DES_UNIDAD
        self.vcContrata = [None]  # DES_CONTRATA
        self.vcPuesto = [None]  # Puesto
        self.dCita = [None]  # dtHoraDeLaCita
        self.tAtencion = [None]
        self.observacion = [None]
        self.fila = 0
        self.muestrasarrive = False
        # TABLA CONTROL DE ACCESO
        # self.vcNombres = None
        # self.vcApellidoPaterno = None
        # self.vcApellidoMaterno = None
        # self.vcCodigoSede = None
        # self.vcSede = None
        self.dtLlegada = None
        self.dtSalida = None
        self.dtCreacion = None
        self.vcUsurarioCreacionDB = None
        # TABLA SEDE AFORO
        # self.vcCodigoSede = None
        self.iAforoActual = 0
        self.AforoGlobal = 0
        # self.dtCreacion = None
        # self.vcUsurarioCreacionDB = None
        # TABLA PACIENTE
        self.biIdPaciente = None
        self.vcNumeroDocumento = None
        self.vcHistoriaClinica = None
        self.dNacimiento = None
        self.cSexo = None
        # self.dtCreacion = None
        # self.vcUsurarioCreacionDB = None
        # TABLA RRRHH
        self.rrhhbiIdMarcacion = None
        self.rrhhbiIdTrabajador = None
        self.rrhhTrabajador = None
        self.rrhhPuesto = None
        self.rrhhEstado = None
        self.rrhhiIdSede = None
        self.rrhhCodigoSede = None
        self.rrhhbCerrado = None
        self.rrhhAforoActual = None

        # FUNCIONES GUI
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.addAction(exitAction)

        # Evaluar conexión al servidor
        self.getIpLocal()
        # Hacer las primeras consultas al servidor
        self.firstconsults()

        self.show()
        self.start()
# FUNCIONES

    def firstconsults(self):
        x = sqlgetdate()
        if x:
            self.DIA = QDateTime.currentDateTime().toString("yyyy-MM-dd")
            self.servidorok = True

            self.sqlgetSEDE()
            self.detectSede()
            print(iAforo)
            # self.iAforo = iAforo[0]
            # self.sede = vcDescripcion[0]
            # self.sedecodigo = vcCodigoSede[0]
            self.display.lblsede.setText(self.sede[0])
            self.display.lblAmax.setText(str(self.iAforo[0]))
            # FALTA PROBAR
            self.sqlgetAforo()
            self.sqlgetAforoArea()
            self.display.lblAmaxArea.setText(str(self.AforoArea))
            self.sqlgetAforoActuralArea()
            self.sqlgetAforoGlobal()
            self.sqlgetTimeOff()
        else:
            print("NO DETECTO SERVIDOR")
            self.imprimir("NO DETECTO SERVIDOR")
            self.servidorok = False
            self.writemensaje = False
        return x
    # FUNCION DE INICIO DEL LOOP

    def start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop)
        self.timer.start(30)
    # BUCLE

    def loop(self):
        # if self.AforoArea == 0 and self.servidorok :
        #   self.firstconsults()
        # self.display.lblNombre.setHidden(False)

        if self.display.DNI != "" and self.display.DNI != "ERRONEO" and self.consult == False and self.reset == False and self.servidorok and self.vip == False and self.rrhh == False:
            self.consult = True
            self.int = 0
            print("CITAAAAA")
            ok = self.sqlgetCITA()
            if ok:
                print(self.display.DNI)
                oki = self.obteneridpaciente()
                if oki:
                    ok1 = self.filtropaciente()
                    if ok1:
                        ok2 = self.filtroingreso()
                        if ok2 == False:
                            ok3 = self.filtroaforo()
                            if ok3:
                                okkk1 = self.sqlwritePaciente_CheckIn()
                                if okkk1:
                                    print("CHECKIN AGREGADO")
                                    # self.sqlrefresh()
                                    self.citacheckin()
                                    self.iAforoActual = self.iAforoActual + 1
                                    okkk4 = self.sqlwriteAforo()
                                    if okkk4:
                                        print("WRITE AFORO TRUE")
                                        self.sqlgetAforoGlobal()
                                    else:
                                        print("WRITE AFORO FALSE")
                                else:
                                    print("FALLA CHECK IN")
                            else:
                                # PERMITIR ACCESO ?
                                print("AFORO LLENO")
                                # self.vip = True
                        else:
                            okkk2 = self.sqlwritePaciente_CheckOut()
                            if okkk2:
                                # self.sqlrefresh()
                                self.citacheckout()
                                print("CHECKOUT TRUE")
                                self.iAforoActual = self.iAforoActual - 1
                                okkk3 = self.sqlwriteAforo()
                                if okkk3:
                                    print("WRITE AFORO TRUE")
                                    self.sqlgetAforoGlobal()
                                else:
                                    print("WRITE AFORO FALSE")
                            else:
                                print("ERROR WRITE CHECKOUT")
                    else:
                        print("ERROR COMPARE CITA")
                        # self.sqlwritePaciente_Control(self.observacion[self.fila] + "," + self.mensaje)
                else:
                    print("ERROR OBTENIENDO ID PACIENTE")
            else:
                # NO TIENE CITA
                self.display.nocita.setHidden(False)
                self.display.lblDNI.setHidden(False)
                print("NOTIENECITA")
                # self.vip = True
# ACTUALIZACION 27/07/20
        elif self.display.DNI != "" and self.display.DNI != "ERRONEO" and self.consult == False and self.reset == False and self.servidorok and self.vip == False and self.rrhh == True:
            self.consult = True
            self.int = 0
            print("RRHH DNI:")
            ok = self.sqlgetEstadoTrabajador()
            if ok:
                print("EXISTE TRABAJADOR")
                ok1 = self.filtrorrhh()
                if ok1:
                    print("TRABAJADOR ACTIVO")
                    ok2 = self.sqlgetID_MARCACION()
                    if ok2:
                        print("SEGUNDA MARCACION")
                        ok3 = self.filtrorrhhsede()
                        if ok3:
                            print("MISMA SEDE")
                            ok4 = self.sqlwriteMarcacionSalida()
                            if ok4:
                                print("MARCACION EXITOSA")
                                self.showasistenciatrue()
                                self.iAforoActual = self.iAforoActual - 1
                                okkk4 = self.sqlwriteAforo()
                                if okkk4:
                                    print("WRITE AFORO TRUE")
                                    self.sqlgetAforoGlobal()
                                else:
                                    print("WRITE AFORO FALSE")
                            else:
                                print("ERROR MARCACION")
                                self.showasistenciafalse()
                        else:
                            print("DISTINTA SEDE")
                            ok4 = self.writesedeanterior()
                            if ok4:
                                print("SEDE ANTERIOR CERRADA")
                                ok5 = self.sqlwriteMarcacionIngreso()
                                if ok5:
                                    print("MARCACION EXITOSA")
                                    self.showasistenciatrue()
                                    self.iAforoActual = self.iAforoActual + 1
                                    okkk4 = self.sqlwriteAforo()
                                    if okkk4:
                                        print("WRITE AFORO TRUE")
                                        self.sqlgetAforoGlobal()
                                    else:
                                        print("WRITE AFORO FALSE")
                                else:
                                    print("ERROR MARCACION")
                                    self.showasistenciafalse()
                            else:
                                print("SEDE ANTERIOR NO CERRADA")

                    else:
                        print("PRIMERA MARCACION")
                        ok3 = self.sqlwriteMarcacionIngreso()
                        if ok3:
                            print("MARCACION EXITOSA")
                            self.showasistenciatrue()
                            self.iAforoActual = self.iAforoActual + 1
                            okkk4 = self.sqlwriteAforo()
                            if okkk4:
                                print("WRITE AFORO TRUE")
                                self.sqlgetAforoGlobal()
                            else:
                                print("WRITE AFORO FALSE")
                        else:
                            print("ERROR MARCACION")
                            self.showasistenciafalse()
                else:
                    print("TRABJAADOR INACTIVO")
            else:
                print("NO EXISTE TRABAJADOR")
                self.showasistenciafalse()

        elif self.display.DNI == "ERRONEO":
            self.display.DNI = ""
            self.consult = True
            self.int = 3
            print("ERRONEO DNI")
            self.erroneoshow("DNI INCORRECTO")
        else:
            # print("ESPERA")
            if self.writemensaje == False and self.servidorok == False:
                self.writemensaje = True
                self.cams = Window1()
                self.cams.show()

        if self.vip:
            self.allowaccess()
        # RESET DE VARIABLES POR CONSULTA
        if self.reset:
            self.sqlgetAforoActuralArea()
            self.reset = False
            self.display.fondo2.setHidden(True)
            self.display.lblNombre.setHidden(True)
            self.display.lblEmpresa.setHidden(True)
            self.display.lblcita.setHidden(True)
            self.display.lblDNI.setHidden(True)
            self.display.fondo1.setHidden(False)
            self.display.nocita.setHidden(True)
            self.display.DNI = ""
            self.display.txtDNI.setText("")

            self.display.recrojo.setHidden(True)
            self.display.nosede.setHidden(True)
            self.display.lblsedecita.setHidden(True)
            self.display.lblestado.setHidden(True)
            self.display.lblestado.setText("")
            self.display.lbllocal.setHidden(True)
            self.display.gracias.setHidden(True)
            self.display.filtrooff.setHidden(True)
            self.display.filtroon.setHidden(True)
            self.display.welcome.setHidden(True)
            self.consult = False
            self.mensaje = ""
            self.vip = False

            self.display.rrhhFalse.setHidden(True)
            self.display.rrhhtrue.setHidden(True)

            # self.AforoArea = 0
            # self.AforoActuralArea = 0

        # TABLA CITA
            self.vcNombres = [None]
            self.vcApellidoPaterno = [None]
            self.vcApellidoMaterno = [None]
            self.idCita = [None]
            self.vcCodigoSede = [None]
            self.vcSede = [None]
            self.vcEstado = [None]
            self.vcCompania = [None]
            self.vcUnidad = [None]
            self.vcContrata = [None]
            self.vcPuesto = [None]
            self.dCita = [None]
            self.tAtencion = [None]
            self.observacion = [None]
            self.fila = 0
        # TABLA CONTROL DE ACCESO
            self.dtLlegada = None
            self.dtSalida = None
            self.dtCreacion = None
            self.vcUsurarioCreacionDB = None
        # TABLA SEDE AFORO
            # self.iAforoActual = None
        # TABLA PACIENTE
            self.biIdPaciente = None
            self.vcNumeroDocumento = None
            self.vcHistoriaClinica = None
            self.dNacimiento = None
            self.cSexo = None
        # TABLA RRHH
            self.rrhhbiIdMarcacion = None
            self.rrhhbiIdTrabajador = None
            self.rrhhTrabajador = None
            self.rrhhPuesto = None
            self.rrhhEstado = None
            self.rrhhiIdSede = None
            self.rrhhCodigoSede = None
            self.rrhhbCerrado = None

        if self.servidorok:
            if self.iAforoActual >= int(self.iAforo[0]):
                self.full = True

        # GENERADOR CLOCK 1Hz
        self.segundos = self.time1.strftime("%S")
        if self.segundos != datetime.datetime.now().strftime("%S"):
            self.time1 = datetime.datetime.now()
            self.clock1s()
            self.display.lblAreal.setText(str(self.iAforoActual))
            self.display.lblArealArea.setText(str(self.AforoActuralArea))
            self.display.lblGlobal.setText(str(self.AforoGlobal))

        if self.clock5s:
            self.clock5s = False
            if self.consult:
                self.consult = False
                self.reset = True

    def allowaccess(self):
        # PERMITIR ACCESO ?

        global global_text
        global win2
        if win2 == False and global_text == "":
            self.cams = Window2()
            self.cams.show()
            win2 = True
            print("AFORO LLENO")
            print("PERMITIR ACCESO ?")

        if global_text == "ADMITIDO":
            okkk1 = self.sqlwritePaciente_CheckIn()
            if okkk1:
                print("CHECKIN AGREGADO")
                self.sqlrefresh()
                self.citacheckin()
                self.iAforoActual = self.iAforoActual + 1
                okkk4 = self.sqlwriteAforo()
                if okkk4:
                    print("WRITE AFORO TRUE")
                    global_text = ""
                else:
                    print("WRITE AFORO FALSE")
                    global_text = ""
            else:
                print("FALLA CHECK IN")
                global_text = ""
        elif global_text == "DENEGADO":
            print("DENEGADO")
            self.sqlwritePaciente_Control(
                self.observacion[self.fila] + ",AFORO LLENO")
            global_text = ""
# CONSULTA AL SERVIDOR

    def obteneridpaciente(self):
        a = False
        okk2 = self.sqlgetID_P()
        if okk2:
            a = True
        else:
            # Write paciente
            print("WRITE PACIENTE")
            okk1 = self.sqlwritePaciente()
            if okk1:
                print("WRITE PACIENTE TRUE")
                # GET ID PACIENTE
                okk2 = self.sqlgetID_P()
                if okk2:
                    a = True
                else:
                    a = False
                    print("ERROR EN OBTENER ID PACIENTE")
            else:
                a = False
                print("ERROR EN ESCRIBIR PACIENTE")

        return a
# FILTROS DE CONSULTA

    def filtrocita(self):
        a = False
        i = 0
        print("FILTRO CITA")
        print(self.sedecodigo)
        while i < len(self.vcCodigoSede):
            if self.observacion[i] == "OK" or self.observacion[i] == "PENDIENTE DE VALIDACION FINANZAS" or self.observacion[i] == "FACTURADO" or self.observacion[i] == "EN REVISION MESA DE AYUDA":
                if self.sedecodigo[0] == self.vcCodigoSede[i]:
                    print(self.sedecodigo[0])
                    self.fila = i
                    a = True
                    return a
                elif self.sedecodigo[1] == self.vcCodigoSede[i]:
                    print(self.sedecodigo[1])
                    self.fila = i
                    a = True
                    return a
            else:
                a = False
            i = i + 1
        return a

    def filtroingreso(self):
        a = False
        okkk = self.sqlgetID_CONTROLACCESO()
        if okkk:
            a = True
            print("CHECKOUT")
        else:
            a = False
            print("CHECKIN")

        return a

    def filtroaforo(self):
        a = False
        if int(self.iAforo[0]) > self.iAforoActual:
            # if int(self.iAforo) > 0:
            print("AFORO TOTAL DECENTE")
            self.sqlgetAforoActuralArea()
            # print(str(self.AforoArea))
            # print(str(self.AforoActuralArea))
            if self.AforoArea > self.AforoActuralArea:
                # if self.AforoArea > 0 :
                a = True
                print("AFORO AREA DECENTE")
            else:
                a = False
                print("AFORO AREA FULL")
                self.recrojoshow("SALA DE ESPERA LLENA")
        else:
            a = False
            print("AFORO FULL")
            self.recrojoshow("AFORO MAXIMO ALCANZADO")

        return a

    def filtropaciente(self):
        a = False
        oka = self.confirmarsede()
        if oka:
            print("CITA EN SEDE CORRECTA")
            oki = self.confirmarestado()
            if oki:
                print("OBSERVACION CORRECTA")
                a = True
                if self.enablefiltro == False:
                    oki1 = self.confirmarhora()
                    if oki1:
                        a = True
                        print("CITA EN LA HORA")
                    else:
                        a = False
                        print("CITA FUERA DE HORA")
                        if self.tAtencion[self.fila] != None:
                            self.recrojoshow(
                                "SU CITA ES A LAS " + str(self.tAtencion[self.fila]))
                        else:
                            self.recrojoshow("LA HORA DE SU CITA ES ERRONEA")
            else:
                a = False
                print("ESTADO NO GENERADO")
                self.recrojoshow(self.observacion[self.fila])
        else:
            a = False
            print("CITA EN SEDE INCORECTA")  # SE MUESTRA EN CONFIRMAR SEDE

        return a

    def recrojoshow(self, data):
        self.sqlwritePaciente_Control(self.observacion[self.fila] + "," + data)
        self.display.lblestado.setText(data)
        self.display.recrojo.setHidden(False)
        self.display.lblestado.setHidden(False)
        self.display.lblDNI.setHidden(False)

    def showasistenciatrue(self):
        print("ASISTENCIA TRUE")
        self.display.lblDNI.setHidden(False)
        self.display.rrhhtrue.setHidden(False)
        self.display.rrhhFalse.setHidden(True)

    def showasistenciafalse(self):
        print("ASISTENCIA FALSE")
        self.display.lblDNI.setHidden(False)
        self.display.rrhhtrue.setHidden(True)
        self.display.rrhhFalse.setHidden(False)


# ACTUALIZACION 27/07/20

    def erroneoshow(self, data):
        self.display.lblestado.setText(data)
        self.display.recrojo.setHidden(False)
        self.display.lblestado.setHidden(False)

    def recverdeshow(self, data):
        self.display.lblestado.setText(data)
        self.display.recrojo.setHidden(False)
        self.display.lblestado.setHidden(False)
# MENSAJE DE INGRESO

    def citacheckin(self):
        nombre = self.vcNombres[self.fila] + " " + \
            self.vcApellidoPaterno[self.fila] + " " + \
            self.vcApellidoMaterno[self.fila]
        self.display.lblNombre.setText(nombre)
        self.display.lblEmpresa.setText(self.vcCompania[self.fila])
        self.display.lblcita.setText(self.tAtencion[self.fila])
        self.display.fondo1.setHidden(True)
        self.display.fondo2.setHidden(False)
        self.display.lblDNI.setHidden(False)
        self.display.lblNombre.setHidden(False)
        self.display.lblEmpresa.setHidden(False)
        self.display.lblcita.setHidden(False)
        self.display.lbllocal.setText(self.vcSede[self.fila])
        self.display.lbllocal.setHidden(False)
        self.display.welcome.setHidden(False)
# MENSAJE DE SALIDA

    def citacheckout(self):
        nombre = self.vcNombres[self.fila] + " " + \
            self.vcApellidoPaterno[self.fila] + " " + \
            self.vcApellidoMaterno[self.fila]
        self.display.gracias.setHidden(False)
        # self.display.lblNombre.setText(nombre)
        # self.display.lblEmpresa.setText(self.vcCompania)
        # self.display.lblcita.setText(self.tAtencion)
        # self.display.fondo1.setHidden(True)
        # self.display.fondo2.setHidden(False)
        self.display.lblDNI.setHidden(False)
        # self.display.lblNombre.setHidden(False)
        # self.display.lblEmpresa.setHidden(False)
        # self.display.lblcita.setHidden(False)
        # self.display.lbllocal.setText(self.vcSede)
        # self.display.lbllocal.setHidden(False)
# FILTRO DE SEDE

    def confirmarsede(self):
        f = False
        # print(self.vcCodigoSede)
        # print(self.sedecodigo)
        if str(self.vcCodigoSede[self.fila]) == str(self.sedecodigo[0]) or str(self.vcCodigoSede[self.fila]) == str(self.sedecodigo[1]):
            # print("SEDE CORRECTA")
            f = True
        else:
            # print("SEDE INCORRECTA")
            f = False
            self.mensaje = "SU CITA ES EN " + self.vcSede[self.fila]
            self.display.lblsedecita.setText(self.vcSede[self.fila])
            self.display.recrojo.setHidden(False)
            self.display.nosede.setHidden(False)
            self.display.lblDNI.setHidden(False)
            self.display.lblsedecita.setHidden(False)
        return f
# FILTRO DE HORA

    def confirmarhora(self):
        x = False
        # HORA ACTUAL
        print("FILTRO DE HORA")
        hoy = datetime.datetime.now()
        print(self.tAtencion[self.fila])
        print(hoy)
        try:
            a = self.tAtencion[self.fila].split(':')
            print("HORA DE ATENCION " + str(a))
            x1 = int(a[0])
            x2 = int(a[1])
            # HORA CITA
            aa = datetime.datetime(hoy.year, hoy.month,
                                   hoy.day, hour=x1, minute=x2)
            af = aa - datetime.timedelta(minutes=30)
            print(str(af))
            if hoy >= af:
                print("PUEDE INGRESAR")
                x = True
            else:
                x = False
                print("LLEGO MUY TEMPRANO")
            return x
        except (Exception) as error:
            print(error)
            return x

# FILTRO DE OBSERVACION DE CITA
    def confirmarestado(self):
        f = False
        print(self.vcEstado)
        print(self.observacion)
        if self.observacion[self.fila] == "OK" or self.observacion[self.fila] == "PENDIENTE DE VALIDACION FINANZAS" or self.observacion[self.fila] == "FACTURADO" or self.observacion[self.fila] == "EN REVISION MESA DE AYUDA":
            print("OBSERVACION OK")
            f = True
        else:
            f = False
            print("OBSERVACION ERRONEA")
        return f

    def clock1s(self):
        self.display.lblhora.setText(
            QDateTime.currentDateTime().toString("hh:mm"))
        self.display.lblfecha.setText(self.DIA)
        if self.consult:
            self.int = self.int + 1
            if self.int == 5:
                self.int = 0
                self.clock5s = True
        else:
            self.int = self.int + 1
            if self.int == 60:
                print("AFORO ACTUALIZADO")
                self.int == 0
                self.sqlgetAforoActuralArea()
                self.sqlgetAforo()

        if self.servidorok == False:
            self.int1 = self.int1 + 1
            if self.int1 == 60:
                self.int1 = 0
                self.firstconsults()

        if self.sayfiltro:
            self.int1 = self.int1 + 1
            if self.int1 == 2:
                self.int1 = 0
                self.sayfiltro = False
                self.reset = True

        if self.timeoff != None:
            pass
            # print(datetime.datetime.now)
            # if datetime.datetime.now().time() >= self.timeoff:
            #    print("OFFF")
            #    os.system('sudo poweroff')


# BOTON PARA DESACTIVAR FILTRO

    @pyqtSlot()
    def btn01_onClick(self):
        if self.enablefiltro:
            self.sayfiltro = True
            self.btn01.setIcon(
                QIcon("/home/pi/PANELNATCLAR/recursos/images/bnt1.png"))
            self.enablefiltro = False
            self.display.filtroon.setHidden(False)

        else:
            self.sayfiltro = True
            self.btn01.setIcon(
                QIcon("/home/pi/PANELNATCLAR/recursos/images/bnt2.png"))
            self.enablefiltro = True
            self.display.filtrooff.setHidden(False)

        self.display.txtDNI.setFocus(True)

    @pyqtSlot()
    def btnnatclar_onClick(self):
        if self.rrhh == False:
            self.btnnatclar.setIcon(
                QIcon("/home/pi/PANELNATCLAR/recursos/images2/natclaroff.jpg"))
            self.rrhh = True
            self.display.fondorrhh.setHidden(False)
            self.display.fondo1.setHidden(True)
            self.display.lblAreal.setHidden(True)
            self.display.lblArealArea.setHidden(True)
            self.display.lblAmax.setHidden(True)
            self.display.lblAmaxArea.setHidden(True)
            self.display.lblGlobal.setHidden(True)
            self.btn01.setHidden(True)
        else:
            self.btnnatclar.setIcon(
                QIcon("/home/pi/PANELNATCLAR/recursos/images2/natclaron.jpg"))
            self.rrhh = False
            self.display.fondorrhh.setHidden(True)
            self.display.fondo1.setHidden(False)
            self.display.lblAreal.setHidden(False)
            self.display.lblArealArea.setHidden(False)
            self.display.lblAmax.setHidden(False)
            self.display.lblAmaxArea.setHidden(False)
            self.display.lblGlobal.setHidden(False)
            self.btn01.setHidden(False)

        self.display.txtDNI.setFocus(True)

# VENTANA DE FALLA DE CONECCION
    @pyqtSlot()
    def buttonWindow2_onClick(self):
        # self.statusBar().showMessage( CONECCION AL SERVIDOR")
        self.cams = Window2()
        self.cams.show()
        self.close()
# CONSULTAS AL SERVIDOR

    def getIpLocal(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.ipLocal = s.getsockname()[0]
        print(self.ipLocal)
        s.close()

    def detectSede(self):
        i = 0
        r = 0
        x = self.ipLocal.split('.')
        print(vcSegmentoRedInferior)
        print(vcSegmentoRedSuperior)
        print(iAforo)
        for a in vcSegmentoRedInferior:
            if a != None:
                if vcSegmentoRedSuperior[i] != None:
                    x1 = vcSegmentoRedInferior[i].split('.')
                    x2 = vcSegmentoRedSuperior[i].split('.')
                    if x[2] >= x1[2] and x[2] <= x2[2]:
                        self.iIdSede[r] = iIdSede[i]
                        self.sede[r] = vcDescripcion[i]
                        self.sedecodigo[r] = vcCodigoSede[i]
                        self.iAforo[r] = iAforo[i]
                        self.sede[r] = self.sede[r].replace("CLINICA ", "")
                        r = r + 1
                else:
                    x1 = vcSegmentoRedInferior[i].split('.')
                    if x[2] == x1[2]:
                        self.iIdSede[r] = iIdSede[i]
                        self.sede[r] = vcDescripcion[i]
                        self.sedecodigo[r] = vcCodigoSede[i]
                        self.iAforo[r] = iAforo[i]
                        self.sede[r] = self.sede[r].replace("CLINICA ", "")
                        r = r + 1
            i = i + 1

        print(self.iIdSede)
        print(self.sedecodigo)
        print(self.sede)

    def sqlgetTimeOff(self):
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute(
                "[dbo].[SP_SEL_HORA_APAGADO_EQUIPO_BY_SEDE] '" + self.sedecodigo[0] + "'")
            results = cursor.fetchone()
            while results:
                a = True
                self.timeoff = results[0]
                print(str(self.timeoff))
                results = cursor.fetchone()
                conn.commit()
            return a

        except (Exception, pyodbc.DatabaseError) as error:
            self.writemensaje = False
            self.servidorok = False
            print(error)
            self.imprimir(error)
            a = False
            return a

    def sqlgetSEDE(self):
        a = False
        i = 0
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute("SELECT iIdSede, vcCodigoSede, vcDescripcion, iIdEstado, vcSegmentoRedInferior, vcSegmentoRedSuperior, iAforo FROM Maestro.SEDE WHERE(iIdEstado = 1) AND(vcSegmentoRedInferior IS NOT NULL)")
            rows = cursor.fetchall()
            # print(rows)
            for row in rows:
                a = True
                print(row)
                iIdSede.append(row[0])
                vcCodigoSede.append(row[1])
                vcDescripcion.append(row[2])
                iIdEstado.append(row[3])
                vcSegmentoRedInferior.append(row[4])
                vcSegmentoRedSuperior.append(row[5])
                iAforo.append(row[6])
                # print(iAforo[i])
                # print("!!!!")
                i = i + 1
                # conn.commit()
            return a

        except (Exception, pyodbc.DatabaseError) as error:
            self.writemensaje = False
            self.servidorok = False
            print(error)
            self.imprimir(error)
            a = False
            return a

        # finally:
            # if conn is not None:
            # conn.close()

    def separetedate(date):
        div = date.split("T")
        fecha = div[0]
        hora = div[1]
        return fecha, hora

    def getestadocita(SiEstadoPago, SiEstado):
        if SiEstadoPago == 1 or SiEstadoPago == 6:
            observacion = "CITA ANULADA POR CLIENTE"
        elif SiEstadoPago == 2 or SiEstadoPago == 5:
            observacion = "OK"
        elif SiEstadoPago == 3 or SiEstadoPago == 4:
            observacion = "PACIENTE NO REGISTRO VOUCHER"
        elif SiEstadoPago == 7:
            observacion = "PENDIENTE DE VALIDACION FINANZAS"

        estado = ["PENDIENTE", "POR CONFIRMAR", "AGENDADO", "EN CURSO",
                  "ATENDIDO", "RE PROGRAMADO", "CANCELADO", "ELIMINADO"]
        return observacion, estado[SiEstado]

    def sqlgetCITA(self):
        a = False
        i = 0
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.33;'
                                  'PORT=1433;'
                                  'DATABASE=CITAS_CHAMAN_20130930;'
                                  'UID=usrRPI;'
                                  'PWD=/elexit0;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            comand = "[dbo].[SP_SEL_CITA_PACIENTE_BY_DNI] '" + \
                self.display.DNI + "','" + self.DIA + "'"
            # print(comand)
            cursor.execute(comand)
            rows = cursor.fetchall()
            # print(rows)
            k = len(rows)
            print(k)

            self.vcNombres = []  # NOMBRES
            self.vcApellidoPaterno = []  # APE_PATERNO
            self.vcApellidoMaterno = []  # APE_MATERNO
            self.vcCodigoSede = []
            self.vcSede = []  # centro
            self.vcEstado = []
            self.vcCompania = []  # DES_COMPANIA
            self.vcUnidad = []  # DES_UNIDAD
            self.vcContrata = []  # DES_CONTRATA
            self.vcPuesto = []  # Puesto
            dtHoraDelLaCita = []  # dtHoraDeLaCita
            self.dCita = []  # dtHoraDeLaCita
            self.tAtencion = []  # dtHoraDeLaCita
            self.observacion = []
            fila = 0
            self.idCita = []

            url = 'https://apinewonline.natclar.com.pe/api/v1/cuenta/login-telemetry'
            body = {'email': 'apereira@costaisa.com', 'password': 'c0sta1s@'}
            x = requests.post(url, json=body)
            a = json.loads(x.text)
            token = a["result"]["token"]

            url = f'https://apinewonline.natclar.com.pe/api/v1/integracion/tiene-cita-en-el-dia?tipoBusqueda=1&DNI={self.display.DNI}'
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = f"Bearer {token}"

            resp = requests.get(url, headers=headers)
            b = json.loads(resp.text)
            rows = b["result"]

            for row in rows:
                self.idCita.append(row["codAgenCita"])
                self.vcNombres.append(row['vcNombres'])  # NOMBRES
                self.vcApellidoPaterno.append(
                    row['vcApellidoPaterno'])  # APE_PATERNO
                self.vcApellidoMaterno.append(row['vcApellidoMaterno'])
                codSede = row['codPcitaId'][0:4]
                self.vcCodigoSede.append(codSede)
                self.vcSede.append(row['centro'])  # centro
                dtHoraDelLaCita.append(row['dtHoraDeLaCita'])  # dtHoraDeLaCita
                fecha, hora = self.separetedate(row['dtHoraDeLaCita'])
                self.dCita.append(fecha)
                self.tAtencion.append(hora)
                h, k = self.getestadocita(row['siEstado'], row['siEstadoPago'])
                self.vcEstado.append(k)
                self.observacion.append(h)
                url = f'https://apinewonline.natclar.com.pe/api/v1/integracion/datos-cita-empresa/{row["codAgenCita"]}'
                headers = CaseInsensitiveDict()
                headers["Accept"] = "application/json"
                headers["Authorization"] = f"Bearer {token}"
                resp = requests.get(url, headers=headers)
                c = json.loads(resp.text)
                self.vcCompania.append(
                    c['result'][0]['DES_COMPANIA'])  # DES_COMPANIA
                self.vcUnidad.append(
                    c['result'][0]['DES_UNIDAD'])  # DES_UNIDAD
                self.vcContrata.append(
                    c['result'][0]['DES_CONTRATA'])  # DES_CONTRATA
                self.vcPuesto.append(c['result'][0]['Puesto'])  # Puesto
            print(self.vcCodigoSede)
            # print(self.tAtencion)
            self.filtrocita()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.writemensaje = False
            self.servidorok = False
            a = False
            return a
        # finally:
         #   if conn is not None:
          #      conn.close()

    def sqlgetID_P(self):
        print("SQL GET ID_P")
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT biIdPaciente FROM PACIENTE WHERE vcNumeroDocumento ='" + self.display.DNI + "'")

            results = cursor.fetchone()
            while results:
                a = True
                self.biIdPaciente = (str(results[0]))
                print("ID PACIENTE " + self.biIdPaciente)
                results = cursor.fetchone()
                conn.commit()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.writemensaje = False
            self.servidorok = False
            a = False
            return a
        finally:
            if conn is not None:
                conn.close()

    def sqlwritePaciente(self):
        a = False
        self.vcNumeroDocumento = self.display.DNI
        self.dtCreacion = datetime.datetime.now()
        self.vcUsurarioCreacionDB = "usrPi"
        # time = date.strftime("%d-%m-%Y %H:%M:%S")
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()

            sql_command = """INSERT INTO PACIENTE (vcNumeroDocumento, dtCreacion, vcUsuarioCreacionDB)
                            VALUES (?, ?, ?);"""

            cursor.execute(sql_command, (self.vcNumeroDocumento,
                                         self.dtCreacion, self.vcUsurarioCreacionDB))

            a = True
            # Commiting any pending transaction to the database.
            conn.commit()
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.writemensaje = False
            self.servidorok = False
            a = False
        # finally:
           # if conn is not None:
            #    conn.close()
        return a

    def sqlgetID_CONTROLACCESO(self):
        print("SQL GET ID CONTROL ACCESO")
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            # cursor.execute("SELECT biIdPacienteControlAcceso FROM [dbo].[PACIENTE_CONTROL_ACCESO] WHERE [dtSalida] IS NULL AND biIdPaciente ='" + self.biIdPaciente + "'" )
            cursor.execute("[dbo].[SP_SEL_PACIENTE_BY_ID] '" +
                           self.biIdPaciente + "'")

            results = cursor.fetchall()
            print(results)
            for r in results:
                a = True
                self.biIdPacienteControlAcceso = (str(r[0]))
                print("IDPACIENTECONTROL " + self.biIdPacienteControlAcceso)
                # results = cursor.fetchone()
                conn.commit()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.writemensaje = False
            self.servidorok = False
            a = False
            return a
        finally:
            if conn is not None:
                conn.close()

    def sqlwritePaciente_CheckIn(self):
        a = False
        self.dtLlegada = datetime.datetime.now()
        self.dtCreacion = datetime.datetime.now()
        self.vcUsurarioCreacionDB = "usrPi"
        # print(self.biIdPaciente)
        # print(self.vcNombres)
        # print(self.vcApellidoMaterno)
        # print(self.idCita)
        # print(self.sedecodigo)
        # print(self.sede)
        # print(self.dtLlegada)
        # print(self.dtCreacion)
        # print(self.observacion)
        # print(self.vcUsurarioCreacionDB)
        # time = date.strftime("%d-%m-%Y %H:%M:%S")
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_command = """INSERT INTO [dbo].[PACIENTE_CONTROL_ACCESO] (biIdPaciente, vcNombres, vcApellidoPaterno, vcApellidoMaterno, idCita, vcCodigoSede, vcSede, dtLlegada, vcObservacion, dtCreacion, vcUsuarioCreacionDB, vcCompania, vcUnidad, vcContrata, vcPuesto, dCita, tAtencion)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(sql_command, (int(self.biIdPaciente), self.vcNombres[self.fila], self.vcApellidoPaterno[self.fila], self.vcApellidoMaterno[self.fila], self.idCita[self.fila], self.sedecodigo[0], self.sede[0], self.dtLlegada,
                                         self.observacion[self.fila], self.dtCreacion, self.vcUsurarioCreacionDB, self.vcCompania[self.fila], self.vcUnidad[self.fila], self.vcContrata[self.fila], self.vcPuesto[self.fila], self.dCita[self.fila], self.tAtencion[self.fila]))
            a = True
            # Commiting any pending transaction to the database.
            conn.commit()
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            a = False
        finally:
            if conn is not None:
                conn.close()
        return a

    def sqlwritePaciente_Control(self, mnsj):
        a = False
        self.dtLlegada = datetime.datetime.now()
        self.dtCreacion = datetime.datetime.now()
        self.vcUsurarioCreacionDB = "usrPi"
        # print(self.biIdPaciente)
        # print(self.vcNombres)
        # print(self.vcApellidoMaterno)
        # print(self.idCita)
        # print(self.sedecodigo)
        # print(self.sede)
        # print(self.dtLlegada)
        # print(self.dtCreacion)
        # print(self.observacion)
        # print(self.vcUsurarioCreacionDB)
        # time = date.strftime("%d-%m-%Y %H:%M:%S")
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_command = """INSERT INTO [control].[PACIENTE_CONTROL_ACCESO] (biIdPaciente, vcNombres, vcApellidoPaterno, vcApellidoMaterno, idCita, vcCodigoSede, vcSede, dtControl, vcObservacion, dtCreacion, vcUsuarioCreacionDB, vcCompania, vcUnidad, vcContrata, vcPuesto, dCita, tAtencion)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

            cursor.execute(sql_command, (int(self.biIdPaciente), self.vcNombres[self.fila], self.vcApellidoPaterno[self.fila], self.vcApellidoMaterno[self.fila], self.idCita[self.fila], self.vcCodigoSede[self.fila], self.vcSede[self.fila],
                                         self.dtLlegada, mnsj, self.dtCreacion, self.vcUsurarioCreacionDB, self.vcCompania[self.fila], self.vcUnidad[self.fila], self.vcContrata[self.fila], self.vcPuesto[self.fila], self.dCita[self.fila], self.tAtencion[self.fila]))
            a = True
            # Commiting any pending transaction to the database.
            conn.commit()
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            a = False
        finally:
            if conn is not None:
                conn.close()
        return a

    def sqlwritePaciente_CheckOut(self):
        a = False
        self.dtSalida = datetime.datetime.now()
        # time = date.strftime("%d-%m-%Y %H:%M:%S")
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_command = "UPDATE PACIENTE_CONTROL_ACCESO SET dtSalida = ? WHERE [dtSalida] IS NULL AND biIdPaciente ='" + \
                self.biIdPaciente + "'"
            cursor.execute(sql_command, self.dtSalida)
            # Commiting any pending transaction to the database.
            a = True
            conn.commit()
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            a = False
        finally:
            if conn is not None:
                conn.close()
        return a

    def sqlwriteAforo(self):
        a = False
        self.dtCreacion = datetime.datetime.now()
        self.vcUsurarioCreacionDB = "usrPi"
        # time = date.strftime("%d-%m-%Y %H:%M:%S")
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_command = """INSERT INTO SEDE_AFORO (vcCodigoSede, iAforo, dtCreacion, vcUsuarioCreacionDB)
                            VALUES (?, ?, ?, ?);"""

            cursor.execute(
                sql_command, (self.sedecodigo[0], self.iAforoActual, self.dtCreacion, self.vcUsurarioCreacionDB))
            a = True
            # Commiting any pending transaction to the database.
            conn.commit()
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            a = False
        finally:
            if conn is not None:
                conn.close()
        return a

    def sqlgetAforo(self):
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute("[dbo].[SP_SEL_AFORO_BY_SEDE] '" +
                           self.sedecodigo[0] + "'")

            results = cursor.fetchone()
            while results:
                a = True
                self.iAforoActual = (results[0])
                print(self.iAforoActual)
                results = cursor.fetchone()
                conn.commit()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.iAforoActual = 0
            a = False
            self.writemensaje = False
            self.servidorok = False
            return a
        finally:
            if conn is not None:
                conn.close()

    def sqlgetAforoArea(self):
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute("[dbo].[SP_SEL_AFORO_BY_SEDE_AREA] '" +
                           self.sedecodigo[0] + "','SALA DE ESPERA'")
            results = cursor.fetchone()
            while results:
                a = True
                self.AforoArea = (results[0])
                print(str(self.AforoArea))
                results = cursor.fetchone()
                conn.commit()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            a = False
            self.writemensaje = False
            self.servidorok = False
            return a
        finally:
            if conn is not None:
                conn.close()

    def sqlgetAforoActuralArea(self):
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute(
                "[dbo].[SP_SEL_PACIENTE_PENDIENTE_CHECKIN_BY_SEDE] '" + self.sedecodigo[0] + "'")
            results = cursor.fetchone()
            while results:
                a = True
                self.AforoActuralArea = (results[0])
                print("AFORO ACTUAL AREA")
                print(str(self.AforoActuralArea))
                results = cursor.fetchone()
                conn.commit()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            a = False
            self.writemensaje = False
            self.servidorok = False
            return a
        # finally:
            # if conn is not None:
            #   conn.close()

    def sqlgetAforoGlobal(self):
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute(
                "[dbo].[SP_SEL_TOTAL_PACIENTES_BY_SEDE] '" + self.sedecodigo[0] + "'")
            results = cursor.fetchone()
            while results:
                a = True
                self.AforoGlobal = (results[0])
                print(self.AforoGlobal)
                results = cursor.fetchone()
                conn.commit()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.AforoGlobal = 0
            a = False
            self.writemensaje = False
            self.servidorok = False
            return a
        finally:
            if conn is not None:
                conn.close()

    def sqlrefresh(self):
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute("[dbo].[SP_EJECUTADOR_CLR]")

        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
        # finally:
            # if conn is not None:
            #   conn.close()

    def imprimir(self, mensaje):
        fecha = datetime.datetime.now()
        ffecha = str(fecha)
        f = open("/home/pi/consolelog.txt", "a")
        f.write("%s  " % ffecha)
        f.write("  %s  " % self.display.DNI)
        f.write("%s\r\n" % mensaje)
        f.close

# FUNCIONES PARA RRRHH
    def sqlgetEstadoTrabajador(self):
        a = False
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrRPIrrhh;'
                                  'PWD=RM@3Hn0ru$sr;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute(
                "[rhControlAcceso].[SP_SEL_TRABAJADOR_BY_DNI]'" + self.display.DNI + "'")
            results = cursor.fetchone()
            while results:
                a = True
                self.rrhhbiIdTrabajador = (str(results[0]))
                self.rrhhTrabajador = (str(results[1]))
                self.rrhhPuesto = (str(results[2]))
                self.rrhhEstado = (str(results[3]))
                results = cursor.fetchone()
                conn.commit()
            return a

        except (Exception, pyodbc.DatabaseError) as error:
            self.writemensaje = False
            self.servidorok = False
            print(error)
            self.imprimir(error)
            a = False
            return a

    def sqlgetID_MARCACION(self):
        print("SQL GET ID_MARCACION")
        a = False
        i = 0
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrRPIrrhh;'
                                  'PWD=RM@3Hn0ru$sr;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute(
                "[rhControlAcceso].[SP_SEL_TRABAJADOR_BY_ID] '" + self.rrhhbiIdTrabajador + "'")

            rows = cursor.fetchall()
            print(rows)
            for row in rows:
                a = True
                self.rrhhbiIdMarcacion = (str(row[0]))
                self.rrhhiIdSede = (str(row[1]))
                self.rrhhbCerrado = (str(row[2]))
                i = i + 1
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.writemensaje = False
            self.servidorok = False
            a = False
            return a
        finally:
            if conn is not None:
                conn.close()

    def sqlwriteMarcacionIngreso(self):
        a = False
        self.dtLlegada = datetime.datetime.now()
        self.dtCreacion = datetime.datetime.now()
        self.vcUsurarioCreacionDB = "usrRPIrrhh"
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrRPIrrhh;'
                                  'PWD=RM@3Hn0ru$sr;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_comand = """INSERT INTO [rhGlobal].[TRABAJADOR_CONTROL_ACCESO](biIdTrabajador, iIdSede, dtLlegada, dtCreacion, vcUsuarioCreacionDB)
                            VALUES(?, ?, ?, ?, ?); """
            cursor.execute(sql_comand, (self.rrhhbiIdTrabajador,
                                        str(self.iIdSede[0]), self.dtLlegada, self.dtCreacion, self.vcUsurarioCreacionDB))

            a = True
            conn.commit()
            return a

        except (Exception, pyodbc.DatabaseError) as error:
            self.writemensaje = False
            self.servidorok = False
            print(error)
            self.imprimir(error)
            a = False
            return a

    def sqlwriteMarcacionSalida(self):
        a = False
        self.dtSalida = datetime.datetime.now()
        self.dtCreacion = datetime.datetime.now()
        self.vcUsurarioCreacionDB = "usrRPIrrhh"
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrRPIrrhh;'
                                  'PWD=RM@3Hn0ru$sr;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_command = "UPDATE [rhGlobal].[TRABAJADOR_CONTROL_ACCESO] SET bCerrado = 1, dtSalida = ? WHERE [dtSalida] IS NULL AND biIdTrabajadorControlAcceso = ?"
            cursor.execute(sql_command, self.dtSalida, self.rrhhbiIdMarcacion)
            a = True
            conn.commit()
            return a

        except (Exception, pyodbc.DatabaseError) as error:
            self.writemensaje = False
            self.servidorok = False
            print(error)
            self.imprimir(error)
            a = False
            return a

    def sqlwriteMarcacionAnterior(self):
        a = False
        self.dtCreacion = datetime.datetime.now()
        print(self.rrhhbiIdMarcacion)
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrRPIrrhh;'
                                  'PWD=RM@3Hn0ru$sr;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_command = "UPDATE [rhGlobal].[TRABAJADOR_CONTROL_ACCESO] SET bCerrado = 1, dtModificacion = ? WHERE [dtSalida] IS NULL AND biIdTrabajadorControlAcceso = " + \
                self.rrhhbiIdMarcacion + " AND iIdSede = " + self.rrhhiIdSede
            cursor.execute(sql_command, self.dtCreacion)
            a = True
            conn.commit()
            return a

        except (Exception, pyodbc.DatabaseError) as error:
            self.writemensaje = False
            self.servidorok = False
            print(error)
            self.imprimir(error)
            a = False
            return a

    def sqlgetSEDERRHH(self):
        a = False
        i = 0
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=NatclarCorporate;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT vcCodigoSede FROM Maestro.SEDE WHERE(iIdEstado = 1) AND(vcSegmentoRedInferior IS NOT NULL) AND(iIdSede = " + self.rrhhiIdSede + ")")
            rows = cursor.fetchall()
            print(rows)
            for row in rows:
                a = True
                self.rrhhCodigoSede = row[0]
                i = i + 1
            return a

        except (Exception, pyodbc.DatabaseError) as error:
            self.writemensaje = False
            self.servidorok = False
            print(error)
            self.imprimir(error)
            a = False
            return a

    def filtrorrhh(self):
        a = False
        if self.rrhhEstado == "ACTIVO":
            a = True
        else:
            a = False
        return a

    def filtrorrhhsede(self):
        a = False
        print("ID SEDES")
        print(self.iIdSede[0])
        print(self.rrhhiIdSede)
        if str(self.rrhhiIdSede) == str(self.iIdSede[0]):
            print("WTF")
            a = True
        else:
            print("aaaaaaF")
            a = False
        return a

    def writesedeanterior(self):
        a = False
        ok = self.sqlwriteMarcacionAnterior()
        if ok:
            a = True
            ok1 = self.sqlgetSEDERRHH()
            if ok1:
                ok2 = self.sqlgetAforoSedeAnterior()
                if ok2:
                    self.rrhhAforoActual = self.rrhhAforoActual - 1
                    ok3 = self.sqlwriteAforoSedeAnterior()
                    if ok3:
                        print("AFORO SEDE ANTERIOR TRUE")
                    else:
                        print("AFORO SEDE ANTERIOR FALSE")
                else:
                    print("GET AFORO SEDE ANTERIOR FALSE")
            else:
                print("GET SEDE ANTERIOR FALSE")
        else:
            print("EEROR WRITEMARCACIONATERIOR")
            a = False

        return a

    def sqlgetAforoSedeAnterior(self):
        a = False
        print("AFORO SEDE ANTEIROR")
        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            cursor.execute("[dbo].[SP_SEL_AFORO_BY_SEDE] '" +
                           self.rrhhCodigoSede + "'")

            results = cursor.fetchone()
            while results:
                a = True
                self.rrhhAforoActual = (results[0])
                print(self.rrhhAforoActual)
                results = cursor.fetchone()
                conn.commit()
            return a
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            self.rrhhAforoActual = 0
            a = False
            self.writemensaje = False
            self.servidorok = False
            return a
        finally:
            if conn is not None:
                conn.close()

    def sqlwriteAforoSedeAnterior(self):
        a = False
        self.dtCreacion = datetime.datetime.now()
        self.vcUsurarioCreacionDB = "usrPi"
        # time = date.strftime("%d-%m-%Y %H:%M:%S")
        print("COMANDO WIRITE")
        print(self.rrhhAforoActual)
        print(self.rrhhCodigoSede)

        try:
            conn = pyodbc.connect('DRIVER={FreeTDS};'
                                  'Server=172.16.1.97;'
                                  'PORT=1433;'
                                  'DATABASE=RPI;'
                                  'UID=usrPix;'
                                  'PWD=Inf@rstdmr@;'
                                  'TDS_Version=7.4')
            cursor = conn.cursor()
            sql_command = """INSERT INTO SEDE_AFORO (vcCodigoSede, iAforo, dtCreacion, vcUsuarioCreacionDB)
                            VALUES (?, ?, ?, ?);"""

            cursor.execute(
                sql_command, (self.rrhhCodigoSede, self.rrhhAforoActual, self.dtCreacion, self.vcUsurarioCreacionDB))
            a = True
            # Commiting any pending transaction to the database.
            conn.commit()
        except (Exception, pyodbc.DatabaseError) as error:
            print(error)
            self.imprimir(error)
            a = False
        finally:
            if conn is not None:
                conn.close()
        return a


class Window1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('INFORMACION')
        self.top = 200
        self.left = 50
        self.width = 300
        self.height = 200

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setWindowIcon(self.style().standardIcon(
            QStyle.SP_FileDialogInfoView))

        # label1 = QLabel()
        self.button = QPushButton("ACEPTAR", self)
        # self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.button.setText("ACEPTAR"))
        self.button.setGeometry(0, 0, 200, 200)
        self.button.clicked.connect(self.close)

        layoutV = QVBoxLayout()
        self.lbl = QLabel(self)
        self.lbl.setFont(QFont("Arial", 14, QFont.Black))
        self.lbl.setGeometry(0, 0, 300, 30)
        self.lbl.setStyleSheet("color : rgb(0, 0, 0)")
        self.lbl.setText("NO HAY CONECCION AL SERVIDOR")  # change label text
        # self.lbl.move(62, 590)
        self.lbl.setHidden(False)
        layoutV.addWidget(self.lbl)

        layoutH = QHBoxLayout()
        # layoutH.addWidget(label1)
        layoutH.addWidget(self.button)
        # layoutH.addWidget(self.button1)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.addAction(exitAction)

        self.show()

    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()


class Window2(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('INFORMACION')
        print("VENTANA 2222")
        self.top = 200
        self.left = 50
        self.width = 300
        self.height = 200

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setWindowIcon(self.style().standardIcon(
            QStyle.SP_FileDialogInfoView))

        self.button = QPushButton("SI", self)
        self.button.setGeometry(0, 0, 200, 200)
        self.button.clicked.connect(self.goMainWindow1)

        self.button1 = QPushButton("NO", self)
        self.button1.setGeometry(0, 0, 200, 200)
        self.button1.clicked.connect(self.goMainWindow2)

        layoutV = QVBoxLayout()
        self.lbl = QLabel(self)
        self.lbl.setFont(QFont("Arial", 14, QFont.Black))
        self.lbl.setGeometry(0, 0, 300, 30)
        self.lbl.setStyleSheet("color : rgb(0, 0, 0)")
        self.lbl.setText("PERMITIR ACCESO")  # change label text
        # self.lbl.move(62, 590)
        self.lbl.setHidden(False)
        layoutV.addWidget(self.lbl)

        layoutH = QHBoxLayout()
        # layoutH.addWidget(label1)
        layoutH.addWidget(self.button)
        layoutH.addWidget(self.button1)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.addAction(exitAction)

        self.show()

    def goMainWindow1(self):
        global global_text
        global win2
        print("ADMITIDO")
        global_text = "ADMITIDO"
        # self.cams = Window()
        # self.cams.show()
        win2 = False
        self.close()

    def goMainWindow2(self):
        global global_text
        global_text = "DENEGADO"
        # self.cams = Window()
        # self.cams.show()
        print("DENEGADO")
        win2 = False
        self.close()


class Window3(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('PERMITIR ACCESO')
        self.setWindowIcon(self.style().standardIcon(
            QStyle.SP_FileDialogInfoView))

        label1 = QLabel(value)
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.button.setIconSize(QSize(200, 200))

        layoutV = QVBoxLayout()
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet(
            'background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText('Click me!')
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)

        layoutH = QHBoxLayout()
        layoutH.addWidget(label1)
        layoutH.addWidget(self.button)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

    def goMainWindow(self):
        self.cams = Window()
        self.cams.show()
        self.close()


if __name__ == '__main__':
    win = Window()
    win.show()
    # win.resize(600,480)
    sys.exit(app.exec_())
    # 280921-v1
