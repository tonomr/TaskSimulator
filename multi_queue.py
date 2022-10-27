import sys
from random import randint
from time import sleep

from PySide6.QtCore import (
    QCoreApplication, QMetaObject, Qt, QObject, QRunnable, QThreadPool, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout,
                               QLabel, QMainWindow, QProgressBar, QPushButton, QWidget, QMessageBox, QComboBox)

from task import Task


class MultiQueueWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        """ Create the widgets to setup the window """
        # Window configuration
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 428)

        # Vars
        self.task_list = []
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(10)
        self.queue_list1 = []
        self.queue_list2 = []

        # Layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        # General Widgets
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setFrameShape(QFrame.Box)
        self.gridLayout.addWidget(
            self.label_title, 1, 1, 1, 5, Qt.AlignHCenter)

        self.label_queue1 = QLabel(self.centralwidget)
        self.label_queue1.setObjectName(u"label_queue1")
        self.label_queue1.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_queue1, 2, 4, 1, 1)

        self.label_queue2 = QLabel(self.centralwidget)
        self.label_queue2.setObjectName(u"label_queue2")
        self.label_queue2.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_queue2, 9, 4, 1, 1)

        self.line_queues = QFrame(self.centralwidget)
        self.line_queues.setObjectName(u"line_queues")
        self.line_queues.setFrameShape(QFrame.HLine)
        self.line_queues.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.line_queues, 8, 0, 1, 5)

        self.line_buttons = QFrame(self.centralwidget)
        self.line_buttons.setObjectName(u"line_buttons")
        self.line_buttons.setFrameShape(QFrame.VLine)
        self.line_buttons.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.line_buttons, 2, 5, 13, 1)

        # P1 Widgets
        self.label_p1 = QLabel(self.centralwidget)
        self.label_p1.setObjectName(u"label_p1")
        self.gridLayout.addWidget(self.label_p1, 2, 0, 1, 1)

        self.label_status_p1 = QLabel(self.centralwidget)
        self.label_status_p1.setObjectName(u"label_status_p1")
        self.gridLayout.addWidget(
            self.label_status_p1, 2, 1, 1, 2, Qt.AlignHCenter)
        
        self.label_time_p1 = QLabel(self.centralwidget)
        self.label_time_p1.setObjectName(u"label_time_p1")
        self.gridLayout.addWidget(self.label_time_p1, 2, 3, 1, 1)

        self.progressBar_p1 = QProgressBar(self.centralwidget)
        self.progressBar_p1.setObjectName(u"progressBar_p1")
        self.progressBar_p1.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p1, 3, 0, 1, 4)

        # P2 Widgtes
        self.label_p2 = QLabel(self.centralwidget)
        self.label_p2.setObjectName(u"label_p2")
        self.gridLayout.addWidget(self.label_p2, 4, 0, 1, 1)

        self.label_status_p2 = QLabel(self.centralwidget)
        self.label_status_p2.setObjectName(u"label_status_p2")
        self.gridLayout.addWidget(
            self.label_status_p2, 4, 1, 1, 2, Qt.AlignHCenter)

        self.label_time_p2 = QLabel(self.centralwidget)
        self.label_time_p2.setObjectName(u"label_time_p2")
        self.gridLayout.addWidget(self.label_time_p2, 4, 3, 1, 1)

        self.progressBar_p2 = QProgressBar(self.centralwidget)
        self.progressBar_p2.setObjectName(u"progressBar_p2")
        self.progressBar_p2.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p2, 5, 0, 1, 4)

        # P3 Widgtes
        self.label_p3 = QLabel(self.centralwidget)
        self.label_p3.setObjectName(u"label_p3")
        self.gridLayout.addWidget(self.label_p3, 6, 0, 1, 1)

        self.label_status_p3 = QLabel(self.centralwidget)
        self.label_status_p3.setObjectName(u"label_status_p3")
        self.gridLayout.addWidget(
            self.label_status_p3, 6, 1, 1, 2, Qt.AlignHCenter)
        
        self.label_time_p3 = QLabel(self.centralwidget)
        self.label_time_p3.setObjectName(u"label_time_p3")
        self.gridLayout.addWidget(self.label_time_p3, 6, 3, 1, 1)

        self.progressBar_p3 = QProgressBar(self.centralwidget)
        self.progressBar_p3.setObjectName(u"progressBar_p3")
        self.progressBar_p3.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p3, 7, 0, 1, 4)

        # P4 Widgets
        self.label_p4 = QLabel(self.centralwidget)
        self.label_p4.setObjectName(u"label_p4")
        self.gridLayout.addWidget(self.label_p4, 9, 0, 1, 1)

        self.label_status_p4 = QLabel(self.centralwidget)
        self.label_status_p4.setObjectName(u"label_status_p4")
        self.gridLayout.addWidget(
            self.label_status_p4, 9, 1, 1, 2, Qt.AlignHCenter)
        
        self.label_time_p4 = QLabel(self.centralwidget)
        self.label_time_p4.setObjectName(u"label_time_p4")
        self.gridLayout.addWidget(self.label_time_p4, 9, 3, 1, 1)
        
        self.progressBar_p4 = QProgressBar(self.centralwidget)
        self.progressBar_p4.setObjectName(u"progressBar_p4")
        self.progressBar_p4.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p4, 10, 0, 1, 4)

        # P5 Widgets
        self.label_p5 = QLabel(self.centralwidget)
        self.label_p5.setObjectName(u"label_p5")
        self.gridLayout.addWidget(self.label_p5, 11, 0, 1, 1)

        self.label_time_p5 = QLabel(self.centralwidget)
        self.label_time_p5.setObjectName(u"label_time_p5")
        self.gridLayout.addWidget(self.label_time_p5, 11, 3, 1, 1)

        self.label_status_p5 = QLabel(self.centralwidget)
        self.label_status_p5.setObjectName(u"label_status_p5")
        self.gridLayout.addWidget(
            self.label_status_p5, 11, 1, 1, 2, Qt.AlignHCenter)

        self.progressBar_p5 = QProgressBar(self.centralwidget)
        self.progressBar_p5.setObjectName(u"progressBar_p5")
        self.progressBar_p5.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p5, 12, 0, 1, 4)

        # P6 Widgets
        self.label_p6 = QLabel(self.centralwidget)
        self.label_p6.setObjectName(u"label_p6")
        self.gridLayout.addWidget(self.label_p6, 13, 0, 1, 1)

        self.label_status_p6 = QLabel(self.centralwidget)
        self.label_status_p6.setObjectName(u"label_status_p6")
        self.gridLayout.addWidget(
            self.label_status_p6, 13, 1, 1, 2, Qt.AlignHCenter)
        
        self.label_time_p6 = QLabel(self.centralwidget)
        self.label_time_p6.setObjectName(u"label_time_p6")
        self.gridLayout.addWidget(self.label_time_p6, 13, 3, 1, 1)

        self.progressBar_p6 = QProgressBar(self.centralwidget)
        self.progressBar_p6.setObjectName(u"progressBar_p6")
        self.progressBar_p6.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p6, 14, 0, 1, 4)

        # ComboBox Widgets
        self.comboBox_group1 = QComboBox(self.centralwidget)
        self.comboBox_group1.addItem("")
        self.comboBox_group1.addItem("")
        self.comboBox_group1.addItem("")
        self.comboBox_group1.addItem("")
        self.comboBox_group1.setObjectName(u"comboBox_group1")
        self.gridLayout.addWidget(self.comboBox_group1, 4, 4, 1, 1)

        self.comboBox_group2 = QComboBox(self.centralwidget)
        self.comboBox_group2.addItem("")
        self.comboBox_group2.addItem("")
        self.comboBox_group2.addItem("")
        self.comboBox_group2.addItem("")
        self.comboBox_group2.setObjectName(u"comboBox_group2")
        self.gridLayout.addWidget(self.comboBox_group2, 11, 4, 1, 1)

        # Buttons Widgets
        self.pushButton_continue = QPushButton(self.centralwidget)
        self.pushButton_continue.setObjectName(u"pushButton_continue")
        self.gridLayout.addWidget(self.pushButton_continue, 3, 6, 1, 1)

        self.pushButton_pause = QPushButton(self.centralwidget)
        self.pushButton_pause.setObjectName(u"pushButton_pause")
        self.gridLayout.addWidget(self.pushButton_pause, 4, 6, 1, 1)

        self.pushButton_finish = QPushButton(self.centralwidget)
        self.pushButton_finish.setObjectName(u"pushButton_finish")
        self.gridLayout.addWidget(self.pushButton_finish, 5, 6, 1, 1)

        self.pushButton_assign = QPushButton(self.centralwidget)
        self.pushButton_assign.setObjectName(u"pushButton_assign")
        self.gridLayout.addWidget(self.pushButton_assign, 10, 6, 1, 1)
        self.pushButton_assign.clicked.connect(self.assign_tasks)

        self.pushButton_execute = QPushButton(self.centralwidget)
        self.pushButton_execute.setObjectName(u"pushButton_execute")
        self.gridLayout.addWidget(self.pushButton_execute, 11, 6, 1, 1)
        self.pushButton_execute.clicked.connect(self.start_execution)

        # Set all widgets in the window
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        """ Set the text in widgets """
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Multi-Queue Manager", None))
        self.label_time_p5.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.comboBox_group1.setItemText(
            0, QCoreApplication.translate("MainWindow", u"FIFO", None))
        self.comboBox_group1.setItemText(
            1, QCoreApplication.translate("MainWindow", u"RR q=3", None))
        self.comboBox_group1.setItemText(
            2, QCoreApplication.translate("MainWindow", u"SJF", None))
        self.comboBox_group1.setItemText(
            3, QCoreApplication.translate("MainWindow", u"LJF", None))

        self.label_status_p5.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_status_p4.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_time_p3.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_queue1.setText(
            QCoreApplication.translate("MainWindow", u"Cola 1", None))
        self.label_p6.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 06", None))
        self.label_p4.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 04", None))
        self.pushButton_assign.setText(QCoreApplication.translate(
            "MainWindow", u"Asignar Procesos", None))
        self.pushButton_pause.setText(
            QCoreApplication.translate("MainWindow", u"Pausar", None))
        self.label_p1.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 01", None))
        self.pushButton_continue.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.label_status_p1.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_status_p3.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_p3.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 03", None))
        self.label_status_p6.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_time_p1.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_status_p2.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.pushButton_execute.setText(
            QCoreApplication.translate("MainWindow", u"Ejecutar", None))
        self.label_time_p4.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_p5.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 05", None))
        self.label_title.setText(QCoreApplication.translate(
            "MainWindow", u"Algoritmo de Planificacion por Colas Multiples", None))
        self.label_time_p2.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_time_p6.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_p2.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 02", None))
        self.pushButton_finish.setText(
            QCoreApplication.translate("MainWindow", u"Terminar", None))
        self.comboBox_group2.setItemText(
            0, QCoreApplication.translate("MainWindow", u"FIFO", None))
        self.comboBox_group2.setItemText(
            1, QCoreApplication.translate("MainWindow", u"RR q=3", None))
        self.comboBox_group2.setItemText(
            2, QCoreApplication.translate("MainWindow", u"SJF", None))
        self.comboBox_group2.setItemText(
            3, QCoreApplication.translate("MainWindow", u"LJF", None))

        self.label_queue2.setText(
            QCoreApplication.translate("MainWindow", u"Cola 2", None))
    # retranslateUi

    def assign_tasks(self) -> None:
        pass

    def start_execution(self) -> None:
        pass


if __name__ == "__main__":
    app = QApplication([])
    window = MultiQueueWindow()
    window.show()
    sys.exit(app.exec())
