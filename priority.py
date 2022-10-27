import sys
from random import randint
from time import sleep

from PySide6.QtCore import (
    QCoreApplication, QMetaObject, Qt, QObject, QRunnable, QThreadPool, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout,
                               QLabel, QMainWindow, QProgressBar, QPushButton, QSpinBox, QWidget, QMessageBox)

from task import Task


class SignalProgress(QObject):
    """ Custom signals for our threads """
    finished = Signal()
    progress = Signal(int)


class RunProgress(QRunnable):
    """ Worker thread for the progress bars """

    def __init__(self, task, status, signal):
        super().__init__()
        self.task = task
        self.status = status
        self.signal = signal
        self.is_paused = False
        self.is_finished = False

    @Slot()
    def run(self):
        """ Run the animations """
        self.status.setText('En Ejecucion')

        for s in range(self.task.execution_time + 1):
            # Send current progress of the bar
            self.signal.progress.emit(
                int((self.task.elapsed_time * 100) / self.task.execution_time))
            sleep(1)
            self.task.elapsed_time += 1

            # Infine loop for pause
            while self.is_paused:
                sleep(0)

            if self.is_finished:
                break

        self.status.setText('Terminado')
    
    def pause(self):
        """ Pause the progression of the bar """
        if not self.is_finished:
            self.is_paused = True
            if self.task.elapsed_time != 0:
                self.status.setText('Bloqueado')

    def resume(self):
        """ Resume the progression of the bar """
        if not self.is_finished:
            self.is_paused = False
            if self.task.elapsed_time != 0:
                self.status.setText('En Ejecucion')

    def finish(self):
        """ Break the progression of the bar """
        self.is_finished = True
        self.status.setText('Terminado')


class RunPrioritys(QRunnable):
    """ Worker thread to run every thread in a list """

    def __init__(self, pool, tasks, signal) -> None:
        super().__init__()
        self.pool = pool
        self.tasks = tasks
        self.signal = signal

    @Slot()
    def run(self):
        """ Run the respective thread in the list in order """
        for t in self.tasks:
            self.pool.start(t)

            while t.is_paused:
                sleep(0)

            if t.is_finished:
                break

            sleep(t.task.execution_time + 1)

        self.signal.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow) -> None:
        """ Set the widgets in the window """
        # Window configuration
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 428)

        # Vars
        self.task_list = []
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(10)
        self.priority_list = []
        self.priority_0 = []
        self.priority_1 = []
        self.priority_2 = []

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

        self.label_priority = QLabel(self.centralwidget)
        self.label_priority.setObjectName(u"label_priority")
        self.gridLayout.addWidget(self.label_priority, 2, 4, 1, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.gridLayout.addWidget(self.line, 2, 5, 12, 1)

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

        self.spinBox_p1 = QSpinBox(self.centralwidget)
        self.spinBox_p1.setObjectName(u"spinBox_p1")
        self.spinBox_p1.setMaximum(2)
        self.gridLayout.addWidget(self.spinBox_p1, 3, 4, 1, 1)

        # P2 Widgets
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

        self.spinBox_p2 = QSpinBox(self.centralwidget)
        self.spinBox_p2.setObjectName(u"spinBox_p2")
        self.spinBox_p2.setMaximum(2)
        self.gridLayout.addWidget(self.spinBox_p2, 5, 4, 1, 1)

        # P3 Widgets
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

        self.spinBox_p3 = QSpinBox(self.centralwidget)
        self.spinBox_p3.setObjectName(u"spinBox_p3")
        self.spinBox_p3.setMaximum(2)
        self.gridLayout.addWidget(self.spinBox_p3, 7, 4, 1, 1)

        # P4 Widgets
        self.label_p4 = QLabel(self.centralwidget)
        self.label_p4.setObjectName(u"label_p4")
        self.gridLayout.addWidget(self.label_p4, 8, 0, 1, 1)

        self.label_status_p4 = QLabel(self.centralwidget)
        self.label_status_p4.setObjectName(u"label_status_p4")
        self.gridLayout.addWidget(
            self.label_status_p4, 8, 1, 1, 2, Qt.AlignHCenter)

        self.label_time_p4 = QLabel(self.centralwidget)
        self.label_time_p4.setObjectName(u"label_time_p4")
        self.gridLayout.addWidget(self.label_time_p4, 8, 3, 1, 1)

        self.progressBar_p4 = QProgressBar(self.centralwidget)
        self.progressBar_p4.setObjectName(u"progressBar_p4")
        self.progressBar_p4.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p4, 9, 0, 1, 4)

        self.spinBox_p4 = QSpinBox(self.centralwidget)
        self.spinBox_p4.setObjectName(u"spinBox_p4")
        self.spinBox_p4.setMaximum(2)
        self.gridLayout.addWidget(self.spinBox_p4, 9, 4, 1, 1)

        # P5 Widgets
        self.label_p5 = QLabel(self.centralwidget)
        self.label_p5.setObjectName(u"label_p5")
        self.gridLayout.addWidget(self.label_p5, 10, 0, 1, 1)

        self.label_status_p5 = QLabel(self.centralwidget)
        self.label_status_p5.setObjectName(u"label_status_p5")
        self.gridLayout.addWidget(
            self.label_status_p5, 10, 1, 1, 2, Qt.AlignHCenter)

        self.label_time_p5 = QLabel(self.centralwidget)
        self.label_time_p5.setObjectName(u"label_time_p5")
        self.gridLayout.addWidget(self.label_time_p5, 10, 3, 1, 1)

        self.progressBar_p5 = QProgressBar(self.centralwidget)
        self.progressBar_p5.setObjectName(u"progressBar_p5")
        self.progressBar_p5.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p5, 11, 0, 1, 4)

        self.spinBox_p5 = QSpinBox(self.centralwidget)
        self.spinBox_p5.setObjectName(u"spinBox_p5")
        self.spinBox_p5.setMaximum(2)
        self.gridLayout.addWidget(self.spinBox_p5, 11, 4, 1, 1)

        # P6 Widgets
        self.label_p6 = QLabel(self.centralwidget)
        self.label_p6.setObjectName(u"label_p6")
        self.gridLayout.addWidget(self.label_p6, 12, 0, 1, 1)

        self.label_status_p6 = QLabel(self.centralwidget)
        self.label_status_p6.setObjectName(u"label_status_p6")
        self.gridLayout.addWidget(
            self.label_status_p6, 12, 1, 1, 2, Qt.AlignHCenter)

        self.label_time_p6 = QLabel(self.centralwidget)
        self.label_time_p6.setObjectName(u"label_time_p6")
        self.gridLayout.addWidget(self.label_time_p6, 12, 3, 1, 1)

        self.progressBar_p6 = QProgressBar(self.centralwidget)
        self.progressBar_p6.setObjectName(u"progressBar_p6")
        self.progressBar_p6.setValue(0)
        self.gridLayout.addWidget(self.progressBar_p6, 13, 0, 1, 4)

        self.spinBox_p6 = QSpinBox(self.centralwidget)
        self.spinBox_p6.setObjectName(u"spinBox_p6")
        self.spinBox_p6.setMaximum(2)
        self.gridLayout.addWidget(self.spinBox_p6, 13, 4, 1, 1)

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
        self.gridLayout.addWidget(self.pushButton_assign, 9, 6, 1, 1)
        self.pushButton_assign.clicked.connect(self.assign_tasks)

        self.pushButton_execute = QPushButton(self.centralwidget)
        self.pushButton_execute.setObjectName(u"pushButton_execute")
        self.gridLayout.addWidget(self.pushButton_execute, 10, 6, 1, 1)
        self.pushButton_execute.clicked.connect(self.start_execution)

        # Set all widgets in window
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow) -> None:
        """ Set the text in widgets """
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Priority Manager", None))
        self.label_p2.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 02", None))
        self.label_status_p4.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_time_p4.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_p3.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 03", None))
        self.pushButton_pause.setText(
            QCoreApplication.translate("MainWindow", u"Pausar", None))
        self.label_status_p5.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_status_p6.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_time_p5.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_status_p1.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_priority.setText(QCoreApplication.translate(
            "MainWindow", u"Prioridad (0-2)", None))
        self.pushButton_execute.setText(
            QCoreApplication.translate("MainWindow", u"Ejecutar", None))
        self.pushButton_finish.setText(
            QCoreApplication.translate("MainWindow", u"Terminar", None))
        self.label_p4.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 04", None))
        self.label_status_p3.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_status_p2.setText(
            QCoreApplication.translate("MainWindow", u"Estado", None))
        self.label_p6.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 06", None))
        self.label_time_p1.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_p5.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 05", None))
        self.label_time_p2.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_time_p3.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_p1.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso 01", None))
        self.label_time_p6.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.pushButton_assign.setText(QCoreApplication.translate(
            "MainWindow", u"Asignar Procesos", None))
        self.pushButton_continue.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.label_title.setText(QCoreApplication.translate(
            "MainWindow", u"Algoritmo de Planificacion por Prioridades", None))
    # retranslateUi

    def assign_tasks(self) -> None:
        """ Create tasks with random times, append to the list and update """
        self.task_list.clear()

        # Create new tasks, then update the labels
        for i in range(6):
            time = randint(3, 12)
            task = Task(i+1, time, 0, time)
            self.task_list.append(task)

        self.label_status_p1.setText('Listo')
        self.label_status_p2.setText('Listo')
        self.label_status_p3.setText('Listo')
        self.label_status_p4.setText('Listo')
        self.label_status_p5.setText('Listo')
        self.label_status_p6.setText('Listo')

        self.label_time_p1.setText(f'{self.task_list[0].execution_time}s')
        self.label_time_p2.setText(f'{self.task_list[1].execution_time}s')
        self.label_time_p3.setText(f'{self.task_list[2].execution_time}s')
        self.label_time_p4.setText(f'{self.task_list[3].execution_time}s')
        self.label_time_p5.setText(f'{self.task_list[4].execution_time}s')
        self.label_time_p6.setText(f'{self.task_list[5].execution_time}s')

        self.progressBar_p1.setValue(0)
        self.progressBar_p2.setValue(0)
        self.progressBar_p3.setValue(0)
        self.progressBar_p4.setValue(0)
        self.progressBar_p5.setValue(0)
        self.progressBar_p6.setValue(0)

        # Make available another run of the program
        self.pushButton_execute.setDisabled(False)
    # assing_tasks

    def start_execution(self) -> None:
        """ Create all threads and signals, execute them """
        if self.task_list:
            self.set_prioritys()

            self.signal_p1 = SignalProgress()
            self.thread_p1 = RunProgress(
                self.task_list[0], self.label_status_p1, self.signal_p1)
            self.thread_p1.signal.progress.connect(self.update_progress_p1)
            self.assign_priority(self.thread_p1)

            self.signal_p2 = SignalProgress()
            self.thread_p2 = RunProgress(
                self.task_list[1], self.label_status_p2, self.signal_p2)
            self.thread_p2.signal.progress.connect(self.update_progress_p2)
            self.assign_priority(self.thread_p2)

            self.signal_p3 = SignalProgress()
            self.thread_p3 = RunProgress(
                self.task_list[2], self.label_status_p3, self.signal_p3)
            self.thread_p3.signal.progress.connect(self.update_progress_p3)
            self.assign_priority(self.thread_p3)

            self.signal_p4 = SignalProgress()
            self.thread_p4 = RunProgress(
                self.task_list[3], self.label_status_p4, self.signal_p4)
            self.thread_p4.signal.progress.connect(self.update_progress_p4)
            self.assign_priority(self.thread_p4)

            self.signal_p5 = SignalProgress()
            self.thread_p5 = RunProgress(
                self.task_list[4], self.label_status_p5, self.signal_p5)
            self.thread_p5.signal.progress.connect(self.update_progress_p5)
            self.assign_priority(self.thread_p5)

            self.signal_p6 = SignalProgress()
            self.thread_p6 = RunProgress(
                self.task_list[5], self.label_status_p6, self.signal_p6)
            self.thread_p6.signal.progress.connect(self.update_progress_p6)
            self.assign_priority(self.thread_p6)

            self.signal_priority_0 = SignalProgress()
            self.thread_priority_0 = RunPrioritys(
                self.thread_pool, self.priority_0, self.signal_priority_0)
            self.thread_priority_0.signal.finished.connect(
                self.finish_priority_0)

            self.signal_priority_1 = SignalProgress()
            self.thread_priority_1 = RunPrioritys(
                self.thread_pool, self.priority_1, self.signal_priority_1)
            self.thread_priority_1.signal.finished.connect(
                self.finish_priority_1)

            self.signal_priority_2 = SignalProgress()
            self.thread_priority_2 = RunPrioritys(
                self.thread_pool, self.priority_2, self.signal_priority_2)
            self.thread_priority_2.signal.finished.connect(
                self.finish_priority_2)
            
            self.pushButton_continue.pressed.connect(self.thread_p1.resume)
            self.pushButton_pause.pressed.connect(self.thread_p1.pause)
            self.pushButton_finish.pressed.connect(self.thread_p1.finish)

            self.pushButton_continue.pressed.connect(self.thread_p2.resume)
            self.pushButton_pause.pressed.connect(self.thread_p2.pause)
            self.pushButton_finish.pressed.connect(self.thread_p2.finish)

            self.pushButton_continue.pressed.connect(self.thread_p3.resume)
            self.pushButton_pause.pressed.connect(self.thread_p3.pause)
            self.pushButton_finish.pressed.connect(self.thread_p3.finish)

            self.pushButton_continue.pressed.connect(self.thread_p4.resume)
            self.pushButton_pause.pressed.connect(self.thread_p4.pause)
            self.pushButton_finish.pressed.connect(self.thread_p4.finish)

            self.pushButton_continue.pressed.connect(self.thread_p5.resume)
            self.pushButton_pause.pressed.connect(self.thread_p5.pause)
            self.pushButton_finish.pressed.connect(self.thread_p5.finish)

            self.pushButton_continue.pressed.connect(self.thread_p6.resume)
            self.pushButton_pause.pressed.connect(self.thread_p6.pause)
            self.pushButton_finish.pressed.connect(self.thread_p6.finish)

            self.thread_pool.start(self.thread_priority_0)

            # Disable buttons while running
            self.pushButton_assign.setDisabled(True)
            self.pushButton_execute.setDisabled(True)
            return

        QMessageBox.warning(self, 'Advertencia',
                            'Asigne procesos primero.')
    # start_execution

    def set_prioritys(self) -> None:
        """ Clear prioritys lists and get the prioritys values in order to assiggn them to the tasks """
        self.priority_list.clear()
        self.priority_0.clear()
        self.priority_1.clear()
        self.priority_2.clear()

        self.priority_list.append(self.spinBox_p1.value())
        self.priority_list.append(self.spinBox_p2.value())
        self.priority_list.append(self.spinBox_p3.value())
        self.priority_list.append(self.spinBox_p4.value())
        self.priority_list.append(self.spinBox_p5.value())
        self.priority_list.append(self.spinBox_p6.value())

        for i in range(6):
            self.task_list[i].priority = self.priority_list[i]
    # set_prioritys

    def assign_priority(self, worker) -> None:
        """ Append threads to respective list for running """
        if worker.task.priority == 0:
            self.priority_0.append(worker)

        elif worker.task.priority == 1:
            self.priority_1.append(worker)

        elif worker.task.priority == 2:
            self.priority_2.append(worker)
    # assign_priority

    # Signals for every progress bar to update values
    def update_progress_p1(self, n) -> None:
        self.progressBar_p1.setValue(n)

    def update_progress_p2(self, n) -> None:
        self.progressBar_p2.setValue(n)

    def update_progress_p3(self, n) -> None:
        self.progressBar_p3.setValue(n)

    def update_progress_p4(self, n) -> None:
        self.progressBar_p4.setValue(n)

    def update_progress_p5(self, n) -> None:
        self.progressBar_p5.setValue(n)

    def update_progress_p6(self, n) -> None:
        self.progressBar_p6.setValue(n)

    # Signals for every priority list to run in order
    def finish_priority_0(self) -> None:
        self.thread_pool.start(self.thread_priority_1)

    def finish_priority_1(self) -> None:
        self.thread_pool.start(self.thread_priority_2)

    def finish_priority_2(self) -> None:
        QMessageBox.information(self, 'Procesos terminados',
                                'Todos los procesos terminaron de ejecutarse.')
        self.pushButton_assign.setDisabled(False)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
