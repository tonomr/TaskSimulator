""" 
virtual-memory_manager.py
Antonio Magaña Reynoso - 218744856
Seminario de Solucion de Problemas de Sistemas Operativos - D05
"""

from sys import exit
from time import sleep

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QRunnable,
                            Qt, QThreadPool, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
                               QLCDNumber, QMainWindow, QProgressBar,
                               QPushButton, QWidget)


class SignalProcess(QObject):
    finished = Signal()


class RunProcess(QRunnable):
    def __init__(self, signal: SignalProcess, blocks: int) -> None:
        super().__init__()
        self.signal = signal
        self.blocks = blocks

    @Slot()
    def run(self) -> None:
        for s in range(9):
            print(f'{s}s')
            sleep(1.0)

        self.signal.finished.emit()


class VirtualMemoryManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    # __init__

    def setupUi(self, MainWindow):
        """ Create the widgets to setup the window """
        # Window configuration
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 320)

        # Layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        # Vars
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(11)

        # Label
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Plain)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_title, 0, 1, 1, 2)

        self.label_tasks_number = QLabel(self.centralwidget)
        self.label_tasks_number.setObjectName(u"label_tasks_number")
        self.label_tasks_number.setFrameShape(QFrame.WinPanel)
        self.label_tasks_number.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_tasks_number, 1, 0, 1, 1)

        self.label_create_tasks = QLabel(self.centralwidget)
        self.label_create_tasks.setObjectName(u"label_create_tasks")
        self.label_create_tasks.setFrameShape(QFrame.WinPanel)
        self.label_create_tasks.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_create_tasks, 1, 2, 1, 1)

        self.label_real_memory = QLabel(self.centralwidget)
        self.label_real_memory.setObjectName(u"label_real_memory")
        self.label_real_memory.setFrameShape(QFrame.WinPanel)
        self.label_real_memory.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_real_memory, 3, 1, 1, 2)

        self.label_virtual_memory = QLabel(self.centralwidget)
        self.label_virtual_memory.setObjectName(u"label_virtual_memory")
        self.label_virtual_memory.setFrameShape(QFrame.WinPanel)
        self.label_virtual_memory.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_virtual_memory, 6, 1, 1, 2)

        # LCDNumber
        self.lcdNumber_tasks_number = QLCDNumber(self.centralwidget)
        self.lcdNumber_tasks_number.setObjectName(u"lcdNumber_tasks_number")
        self.lcdNumber_tasks_number.setFrameShadow(QFrame.Plain)
        self.lcdNumber_tasks_number.setSegmentStyle(QLCDNumber.Flat)
        self.gridLayout.addWidget(self.lcdNumber_tasks_number, 2, 0, 1, 1)

        # PushButton
        self.pushButton_new_task2b = QPushButton(self.centralwidget)
        self.pushButton_new_task2b.setObjectName(u"pushButton_new_task2b")
        self.gridLayout.addWidget(self.pushButton_new_task2b, 2, 1, 1, 1)
        self.pushButton_new_task2b.clicked.connect(
            lambda: self.create_task(20))

        self.pushButton_new_task4b = QPushButton(self.centralwidget)
        self.pushButton_new_task4b.setObjectName(u"pushButton_new_task4b")
        self.gridLayout.addWidget(self.pushButton_new_task4b, 2, 2, 1, 1)
        self.pushButton_new_task4b.clicked.connect(
            lambda: self.create_task(40))

        self.pushButton_new_task6b = QPushButton(self.centralwidget)
        self.pushButton_new_task6b.setObjectName(u"pushButton_new_task6b")
        self.gridLayout.addWidget(self.pushButton_new_task6b, 2, 3, 1, 1)
        self.pushButton_new_task6b.clicked.connect(
            lambda: self.create_task(60))

        # Line
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.line, 5, 0, 1, 4)

        # ProgressBar
        self.progressBar_real_memory = QProgressBar(self.centralwidget)
        self.progressBar_real_memory.setObjectName(u"progressBar_real_memory")
        self.progressBar_real_memory.setValue(0)
        self.gridLayout.addWidget(self.progressBar_real_memory, 4, 0, 1, 4)

        self.progressBar_virtual_memory = QProgressBar(self.centralwidget)
        self.progressBar_virtual_memory.setObjectName(
            u"progressBar_virtual_memory")
        self.progressBar_virtual_memory.setValue(0)
        self.gridLayout.addWidget(self.progressBar_virtual_memory, 7, 0, 1, 4)

        # Set all widgets in the window
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Virtual Memory Manager - AMR", None))
        self.label_title.setText(QCoreApplication.translate(
            "MainWindow", u"Administrador de Memoria Virtual", None))
        self.label_tasks_number.setText(QCoreApplication.translate(
            "MainWindow", u"Procesos en Memoria", None))
        self.label_create_tasks.setText(QCoreApplication.translate(
            "MainWindow", u"Crear Nuevos  Procesos", None))
        self.pushButton_new_task2b.setText(QCoreApplication.translate("MainWindow", u"Crear nuevo \n"
                                                                      "proceso (2 bloques)", None))
        self.pushButton_new_task4b.setText(QCoreApplication.translate("MainWindow", u"Crear nuevo \n"
                                                                      "proceso (4 bloques)", None))
        self.pushButton_new_task6b.setText(QCoreApplication.translate("MainWindow", u"Crear nuevo \n"
                                                                      "proceso (6 bloques)", None))
        self.label_real_memory.setText(QCoreApplication.translate(
            "MainWindow", u"Memoria Real Ocupada", None))
        self.progressBar_real_memory.setFormat(
            QCoreApplication.translate("MainWindow", u"%p%", None))
        self.label_virtual_memory.setText(QCoreApplication.translate(
            "MainWindow", u"Memoria Virtual Ocupada", None))
        self.progressBar_virtual_memory.setFormat(
            QCoreApplication.translate("MainWindow", u"%p%", None))
    # retranslateUi

    def create_task(self, blocks: int) -> None:
        real_mem_cap = self.progressBar_real_memory.value() + blocks
        virtual_mem_cap = self.progressBar_virtual_memory.value() + blocks
        if real_mem_cap <= 100:
            print(f'enough r-memory for {blocks}blocks')
            self.lcdNumber_tasks_number.display(
                self.lcdNumber_tasks_number.intValue() + 1)
            self.progressBar_real_memory.setValue(
                self.progressBar_real_memory.value() + blocks)
            signal = SignalProcess()
            process = RunProcess(signal, blocks)
            process.signal.finished.connect(
                lambda: self.finish_task_real(blocks))

            self.thread_pool.start(process)

        else:
            if virtual_mem_cap <= 100:
                print(f'enough v-memory for {blocks}blocks')
                self.lcdNumber_tasks_number.display(
                    self.lcdNumber_tasks_number.intValue() + 1)
                self.progressBar_virtual_memory.setValue(
                    self.progressBar_virtual_memory.value() + blocks)
                signal = SignalProcess()
                process = RunProcess(signal, blocks)
                process.signal.finished.connect(
                    lambda: self.finish_task_virtual(blocks))

                self.thread_pool.start(process)
            else:
                print(f'not enough memory for {blocks}blocks')

    # create_task

    def finish_task_real(self, blocks: int):
        print('finished')
        self.progressBar_real_memory.setValue(
            self.progressBar_real_memory.value() - blocks)
        self.lcdNumber_tasks_number.display(
            self.lcdNumber_tasks_number.intValue() - 1)
    # finish_task_real

    def finish_task_virtual(self, blocks: int):
        print('finished')
        self.progressBar_virtual_memory.setValue(
            self.progressBar_virtual_memory.value() - blocks)
        self.lcdNumber_tasks_number.display(
            self.lcdNumber_tasks_number.intValue() - 1)
    # finish_task_virtual


if __name__ == '__main__':
    app = QApplication([])
    window = VirtualMemoryManagerWindow()
    window.show()
    exit(app.exec())
