#By: Jose R. Prieto Fontcuberta
from PyQt4 import QtCore, QtGui, uic, QtOpenGL

import subprocess
import os,sys,threading

Ui_MainWindow, QMainWindow = uic.loadUiType("gui.ui")
subprocess.call(["ls", "-l"], shell=True)


class Ui_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.runManagers.clicked.connect(self.startManager)
        self.runAgents.clicked.connect(self.startAgents)
        self.applyConfigs.clicked.connect(self.configuraciones)
        self.nAgentes = 2
        self.map = ""
        self.refresh = 125
        self.duracion = 10

        # Allied
        self.allied_Soldados = 1
        self.allied_Medicos = 1
        self.allied_Fieldops = 1
        # Axis
        self.axis_Soldados = 1
        self.axis_Medicos = 1
        self.axis_Fieldops = 1
        self.cwd = self.jgomas_input.text()
        self.configuraciones()
        #"D:\\AIN\\Practicas\\jgomas\\bin\mas"

    def configuraciones(self):
        self.getData()
        self.cwd = self.jgomas_input.text()
        self.maps_directory = self.mapDirectory_input.text()
        maps = self.getMaps()
        self.mapNameBox.addItems(maps)

    def getData(self):

        self.nAgentes = self.nAgentesEdit.value()
        self.map = self.mapNameBox.currentText()
        self.refresh = int(self.refreshEdit.text())
        self.duracion = int(self.duracionEdit.text())

        # Allied
        self.allied_Fieldops = self.alliedFieldops.value()
        self.allied_Medicos = self.alliedMedicos.value()
        self.allied_Soldados = self.alliedSoldados.value()

        # Axis
        self.axis_Fieldops = self.axisFieldops.value()
        self.axis_Medicos = self.axisMedicos.value()
        self.axis_Soldados = self.axisSoldados.value()
#/home/jose/AIN/ain/bin/data/maps
    def getMaps(self):
        self.getData()
        print('ls {}'.format(self.maps_directory))
        a = os.popen('ls {}'.format(self.maps_directory)).read()
        a = a.split('\n')
        a = a[:-1]
        return a



    def startManager(self):
        self.getData()
        if not self.checkLinux.isChecked(): #Windows
            managerString = "java -classpath lib\jade.jar;lib\jadeTools.jar;lib\Base64.jar;lib\http.jar;lib\iiop.jar;lib\\beangenerator.jar;lib\jgomas.jar;lib\jason.jar;lib\JasonJGomas.jar;classes;. jade.Boot -gui Manager:es.upv.dsic.gti_ia.jgomas.CManager({0},{1},{2},{3})".format(self.nAgentes,self.map,self.refresh,self.duracion)
        else: #Linux
            managerString = "java -classpath \"lib/jade.jar:lib/jadeTools.jar:lib/Base64.jar:lib/http.jar:lib/iiop.jar:lib/beangenerator.jar:lib/jgomas.jar:lib/jason.jar:lib/JasonJGomas.jar:classes:.\" jade.Boot -gui -host 127.0.0.1 \"Manager:es.upv.dsic.gti_ia.jgomas.CManager({0},{1},{2},{3})\"".format(self.nAgentes,self.map,self.refresh,self.duracion)

        print(managerString)
        print(managerString.split())
        self.managerOutput.clear()
        self.managerOutput.insertPlainText(managerString)
        manager = Comand(self.cwd, managerString)
        if self.checkBoxManagerStart.isChecked():
            manager.start()

    def startAgents(self):
        self.getData()
        print("Setting agents")
        if not self.checkLinux.isChecked():  # Windows
            agentsString = "java -classpath lib\jade.jar;lib\jadeTools.jar;lib\Base64.jar;lib\http.jar;lib\iiop.jar;lib\beangenerator.jar;lib\jgomas.jar;student.jar;lib\jason.jar;lib\JasonJGomas.jar;classes;. jade.Boot -container -host localhost "
        else:  # Linux
            agentsString = "java -classpath \"lib/jade.jar:lib/jadeTools.jar:lib/Base64.jar:lib/http.jar:lib/iiop.jar:lib/beangenerator.jar:lib/jgomas.jar:student.jar:lib/jason.jar:lib/JasonJGomas.jar:classes:.\" jade.Boot -container -host 127.0.0.1 \""

        #agentsString += "\""

        AxisMedics = ''.join(
            ["TM{0}:es.upv.dsic.gti_ia.JasonJGomas.BasicTroopJasonArch(jasonAgent_AXIS_MEDIC.asl);".format(i) for i in
             range(self.axis_Medicos)])
        AxisSoldiers = ''.join(
            ["TS{0}:es.upv.dsic.gti_ia.JasonJGomas.BasicTroopJasonArch(jasonAgent_AXIS.asl);".format(i) for i in
             range(self.axis_Soldados)])
        AxisFieldops = ''.join(
            ["TF{0}:es.upv.dsic.gti_ia.JasonJGomas.BasicTroopJasonArch(jasonAgent_AXIS_FIELDOPS.asl);".format(i) for i
             in range(self.axis_Fieldops)])
        agentsString += AxisMedics + AxisSoldiers + AxisFieldops

        AlliedMedics = ''.join(
            ["AM{0}:es.upv.dsic.gti_ia.JasonJGomas.BasicTroopJasonArch(jasonAgent_ALLIED_MEDIC.asl);".format(i) for i in
             range(self.allied_Medicos)])
        AlliedSoldiers = ''.join(
            ["AS{0}:es.upv.dsic.gti_ia.JasonJGomas.BasicTroopJasonArch(jasonAgent_ALLIED.asl);".format(i) for i in
             range(self.allied_Soldados)])
        AlliedFieldops = ''.join(
            ["AF{0}:es.upv.dsic.gti_ia.JasonJGomas.BasicTroopJasonArch(jasonAgent_ALLIED_FIELDOPS.asl);".format(i) for i
             in range(self.allied_Fieldops)])
        agentsString += AlliedMedics + AlliedSoldiers + AlliedFieldops
        if self.checkLinux.isChecked():
            agentsString +="\""
        print(agentsString)

        #agentsString += "\""
        self.botsOutput.clear()
        self.botsOutput.insertPlainText(agentsString)
        agents = Comand(self.cwd, agentsString)
        if self.checkBoxBotsStart.isChecked():
            agents.start()
        #sys.exit(0)



class Comand(threading.Thread):
    def __init__(self,cwd,comands):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)
        self.cwd = cwd
        self.comand = comands

    def run(self):
        print("Llamando a %s" % self.comand.split())
        p = subprocess.Popen(self.comand.split(), shell=True, cwd=self.cwd,creationflags=subprocess.CREATE_NEW_CONSOLE)
        sts = os.waitpid(p.pid, 0)



app = QtGui.QApplication(sys.argv)
MyWindow = Ui_MainWindow(None)
MyWindow.show()
app.exec_()