from random import randint
from time import sleep

from PySide6.QtCore import QCoreApplication, QMetaObject, QObject, QRect, Signal, Slot, QRunnable, QThreadPool
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QWidget, QMessageBox

from task import Task


class WorkerSignals(QObject):
    progress = Signal(int)


class JobRunner(QRunnable):
    def __init__(self, task, signal, status):
        super().__init__()
        self.task = task
        self.signal = signal
        self.status = status
        self.is_paused = False
        self.is_killed = False

    @Slot()
    def run(self):
        for s in range(self.task.execution_time+1):
            self.signal.progress.emit(int((self.task.elapsed_time*100) / self.task.execution_time))
            self.task.elapsed_time += 1
            sleep(1)

            while self.is_paused:
                sleep(0)

            if self.is_killed:
                break

            if s == self.task.execution_time-1:
                self.status.setText('Terminado')
        
        self.is_killed = True
        self.status.setText('Terminado')

    def pause(self):
        if not self.is_killed:
            self.is_paused = True
            self.status.setText('Bloqueado')

    def resume(self):
        if not self.is_killed:
            self.is_paused = False
            self.status.setText('Corriendo')

    def kill(self):
        self.is_killed = True
        self.status.setText('Terminado')


class Ui_Manager(object):
    def setupUi(self, MainWindow):
        # Variables
        self.task_list = []
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(5)

        # MainWindow Configs
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        self.container = QWidget(MainWindow)
        self.container.setObjectName(u"container")
        
        # Left Grid Layout
        self.widget = QWidget(self.container)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(11, 60, 351, 241))     
        self.gridLayout_left = QGridLayout(self.widget)
        self.gridLayout_left.setObjectName(u"gridLayout_left")
        self.gridLayout_left.setContentsMargins(0, 0, 0, 0)

        # Right Grid Layout
        self.widget1 = QWidget(self.container)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(360, 60, 231, 241))
        self.gridLayout_right = QGridLayout(self.widget1)
        self.gridLayout_right.setObjectName(u"gridLayout_right")
        self.gridLayout_right.setContentsMargins(0, 0, 0, 0)

        # Horizontal Layout Bottom
        self.widget2 = QWidget(self.container)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(90, 330, 411, 25))
        self.horizontalLayout_bottom = QHBoxLayout(self.widget2)
        self.horizontalLayout_bottom.setObjectName(u"horizontalLayout_bottom")
        self.horizontalLayout_bottom.setContentsMargins(0, 0, 0, 0)

        # Left Widgets
        ## Labels Proccess
        self.label_p1 = QLabel(self.widget)
        self.label_p1.setObjectName(u"label_p1")
        self.gridLayout_left.addWidget(self.label_p1, 0, 0, 1, 1)

        self.label_p2 = QLabel(self.widget)
        self.label_p2.setObjectName(u"label_p2")
        self.gridLayout_left.addWidget(self.label_p2, 2, 0, 1, 1)

        self.label_p3 = QLabel(self.widget)
        self.label_p3.setObjectName(u"label_p3")
        self.gridLayout_left.addWidget(self.label_p3, 4, 0, 1, 1)

        self.label_p4 = QLabel(self.widget)
        self.label_p4.setObjectName(u"label_p4")
        self.gridLayout_left.addWidget(self.label_p4, 6, 0, 1, 1)

        ## Labels Status
        self.label_status_1 = QLabel(self.widget)
        self.label_status_1.setObjectName(u"label_status_1")
        self.gridLayout_left.addWidget(self.label_status_1, 0, 1, 1, 1)

        self.label_status_2 = QLabel(self.widget)
        self.label_status_2.setObjectName(u"label_status_2")
        self.gridLayout_left.addWidget(self.label_status_2, 2, 1, 1, 1)

        self.label_status_3 = QLabel(self.widget)
        self.label_status_3.setObjectName(u"label_status_3")
        self.gridLayout_left.addWidget(self.label_status_3, 4, 1, 1, 1)

        self.label_status_4 = QLabel(self.widget)
        self.label_status_4.setObjectName(u"label_status_4")
        self.gridLayout_left.addWidget(self.label_status_4, 6, 1, 1, 1)

        ## Labels Times
        self.label_time_1 = QLabel(self.widget)
        self.label_time_1.setObjectName(u"label_time_1")
        self.gridLayout_left.addWidget(self.label_time_1, 0, 2, 1, 1)

        self.label_time_2 = QLabel(self.widget)
        self.label_time_2.setObjectName(u"label_time_2")
        self.gridLayout_left.addWidget(self.label_time_2, 2, 2, 1, 1)

        self.label_time_3 = QLabel(self.widget)
        self.label_time_3.setObjectName(u"label_time_3")
        self.gridLayout_left.addWidget(self.label_time_3, 4, 2, 1, 1)

        self.label_time_4 = QLabel(self.widget)
        self.label_time_4.setObjectName(u"label_time_4")
        self.gridLayout_left.addWidget(self.label_time_4, 6, 2, 1, 1)

        ## Progressbars
        self.progressBar_p1 = QProgressBar(self.widget)
        self.progressBar_p1.setObjectName(u"progressBar_p1")
        self.gridLayout_left.addWidget(self.progressBar_p1, 1, 0, 1, 3)

        self.progressBar_p2 = QProgressBar(self.widget)
        self.progressBar_p2.setObjectName(u"progressBar_p2")
        self.gridLayout_left.addWidget(self.progressBar_p2, 3, 0, 1, 3)

        self.progressBar_p3 = QProgressBar(self.widget)
        self.progressBar_p3.setObjectName(u"progressBar_p3")
        self.gridLayout_left.addWidget(self.progressBar_p3, 5, 0, 1, 3)

        self.progressBar_p4 = QProgressBar(self.widget)
        self.progressBar_p4.setObjectName(u"progressBar_p4")
        self.gridLayout_left.addWidget(self.progressBar_p4, 7, 0, 1, 3)

        # Right Widgets
        ## Pause Buttons
        self.pushButton_pause_p1 = QPushButton(self.widget1)
        self.pushButton_pause_p1.setObjectName(u"pushButton_pause_p1")
        self.gridLayout_right.addWidget(self.pushButton_pause_p1, 0, 0, 1, 1)

        self.pushButton_pause_p2 = QPushButton(self.widget1)
        self.pushButton_pause_p2.setObjectName(u"pushButton_pause_p2")
        self.gridLayout_right.addWidget(self.pushButton_pause_p2, 1, 0, 1, 1)

        self.pushButton_pause_p3 = QPushButton(self.widget1)
        self.pushButton_pause_p3.setObjectName(u"pushButton_pause_p3")
        self.gridLayout_right.addWidget(self.pushButton_pause_p3, 2, 0, 1, 1)

        self.pushButton_pause_p4 = QPushButton(self.widget1)
        self.pushButton_pause_p4.setObjectName(u"pushButton_pause_p4")
        self.gridLayout_right.addWidget(self.pushButton_pause_p4, 3, 0, 1, 1)
        

        ## Resume Buttons
        self.pushButton_resume_p1 = QPushButton(self.widget1)
        self.pushButton_resume_p1.setObjectName(u"pushButton_resume_p1")
        self.gridLayout_right.addWidget(self.pushButton_resume_p1, 0, 1, 1, 1)

        self.pushButton_resume_p2 = QPushButton(self.widget1)
        self.pushButton_resume_p2.setObjectName(u"pushButton_resume_p2")
        self.gridLayout_right.addWidget(self.pushButton_resume_p2, 1, 1, 1, 1)

        self.pushButton_resume_p3 = QPushButton(self.widget1)
        self.pushButton_resume_p3.setObjectName(u"pushButton_resume_p3")
        self.gridLayout_right.addWidget(self.pushButton_resume_p3, 2, 1, 1, 1)

        self.pushButton_resume_p4 = QPushButton(self.widget1)
        self.pushButton_resume_p4.setObjectName(u"pushButton_resume_p4")
        self.gridLayout_right.addWidget(self.pushButton_resume_p4, 3, 1, 1, 1)
        

        ## Kill Buttons
        self.pushButton_kill_p1 = QPushButton(self.widget1)
        self.pushButton_kill_p1.setObjectName(u"pushButton_kill_p1")
        self.gridLayout_right.addWidget(self.pushButton_kill_p1, 0, 2, 1, 1)

        self.pushButton_kill_p2 = QPushButton(self.widget1)
        self.pushButton_kill_p2.setObjectName(u"pushButton_kill_p2")
        self.gridLayout_right.addWidget(self.pushButton_kill_p2, 1, 2, 1, 1)

        self.pushButton_kill_p3 = QPushButton(self.widget1)
        self.pushButton_kill_p3.setObjectName(u"pushButton_kill_p3")
        self.gridLayout_right.addWidget(self.pushButton_kill_p3, 2, 2, 1, 1)

        self.pushButton_kill_p4 = QPushButton(self.widget1)
        self.pushButton_kill_p4.setObjectName(u"pushButton_kill_p4")
        self.gridLayout_right.addWidget(self.pushButton_kill_p4, 3, 2, 1, 1)
        
        
        # Bottom Widgets
        ## Assign Tasks Button
        self.pushButton_assign_tasks = QPushButton(self.widget2)
        self.pushButton_assign_tasks.setObjectName(u"pushButton_assign_tasks")
        self.horizontalLayout_bottom.addWidget(self.pushButton_assign_tasks)
        self.pushButton_assign_tasks.clicked.connect(self.assign_tasks)

        ## Start Processing Button
        self.pushButton_start_processing = QPushButton(self.widget2)
        self.pushButton_start_processing.setObjectName(u"pushButton_start_processing")
        self.horizontalLayout_bottom.addWidget(self.pushButton_start_processing)
        self.pushButton_start_processing.clicked.connect(self.start_execution)

        # Show Widgets
        MainWindow.setCentralWidget(self.container)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Administrador de Procesos", None))
        self.label_p1.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso #1", None))
        self.label_time_2.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_p2.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso #2", None))
        self.label_p3.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso #3", None))
        self.label_status_1.setText(QCoreApplication.translate(
            "MainWindow", u"\u00bfEstado?", None))
        self.label_status_3.setText(QCoreApplication.translate(
            "MainWindow", u"\u00bfEstado?", None))
        self.label_time_1.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_status_2.setText(QCoreApplication.translate(
            "MainWindow", u"\u00bfEstado?", None))
        self.label_time_3.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.label_p4.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso #4", None))
        self.label_status_4.setText(QCoreApplication.translate(
            "MainWindow", u"\u00bfEstado?", None))
        self.label_time_4.setText(
            QCoreApplication.translate("MainWindow", u"0s", None))
        self.pushButton_pause_p1.setText(
            QCoreApplication.translate("MainWindow", u"Pausa", None))
        self.pushButton_resume_p1.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.pushButton_kill_p1.setText(
            QCoreApplication.translate("MainWindow", u"Terminar", None))
        self.pushButton_pause_p2.setText(
            QCoreApplication.translate("MainWindow", u"Pausa", None))
        self.pushButton_resume_p2.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.pushButton_kill_p2.setText(
            QCoreApplication.translate("MainWindow", u"Terminar", None))
        self.pushButton_pause_p3.setText(
            QCoreApplication.translate("MainWindow", u"Pausa", None))
        self.pushButton_resume_p3.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.pushButton_kill_p3.setText(
            QCoreApplication.translate("MainWindow", u"Terminar", None))
        self.pushButton_pause_p4.setText(
            QCoreApplication.translate("MainWindow", u"Pausa", None))
        self.pushButton_resume_p4.setText(
            QCoreApplication.translate("MainWindow", u"Continuar", None))
        self.pushButton_kill_p4.setText(
            QCoreApplication.translate("MainWindow", u"Terminar", None))
        self.pushButton_assign_tasks.setText(
            QCoreApplication.translate("MainWindow", u"Asignar Procesos", None))
        self.pushButton_start_processing.setText(
            QCoreApplication.translate("MainWindow", u"Empezar Procesamiento", None))
    # retranslateUi

    def assign_tasks(self):
        # Fill the task list
        for i in range(4):
            exec_time = randint(2, 12)
            task = Task(i+1, exec_time, 0, exec_time)
            self.task_list.append(task)

        self.label_time_1.setText(f'{self.task_list[0].execution_time}s')
        self.label_status_1.setText(f'Nuevo')
        self.label_status_1.setText(f'Listo')
        self.label_time_2.setText(f'{self.task_list[1].execution_time}s')
        self.label_status_2.setText(f'Nuevo')
        self.label_status_2.setText(f'Listo')
        self.label_time_3.setText(f'{self.task_list[2].execution_time}s')
        self.label_status_3.setText(f'Nuevo')
        self.label_status_3.setText(f'Listo')
        self.label_time_4.setText(f'{self.task_list[3].execution_time}s')
        self.label_status_4.setText(f'Nuevo')
        self.label_status_4.setText(f'Listo')

    def start_execution(self):
        if self.task_list:
            self.signal_p1 = WorkerSignals()
            self.runner_p1 = JobRunner(self.task_list[0], self.signal_p1, self.label_status_1)
            self.pushButton_pause_p1.pressed.connect(self.runner_p1.pause)
            self.pushButton_resume_p1.pressed.connect(self.runner_p1.resume)
            self.pushButton_kill_p1.pressed.connect(self.runner_p1.kill)
            self.runner_p1.signal.progress.connect(self.update_progress_p1)

            self.signal_p2 = WorkerSignals()
            self.runner_p2 = JobRunner(self.task_list[1], self.signal_p2, self.label_status_2)
            self.pushButton_pause_p2.pressed.connect(self.runner_p2.pause)
            self.pushButton_resume_p2.pressed.connect(self.runner_p2.resume)
            self.pushButton_kill_p2.pressed.connect(self.runner_p2.kill)
            self.runner_p2.signal.progress.connect(self.update_progress_p2)

            self.signal_p3 = WorkerSignals()
            self.runner_p3 = JobRunner(self.task_list[2], self.signal_p3, self.label_status_3)
            self.pushButton_pause_p3.pressed.connect(self.runner_p3.pause)
            self.pushButton_resume_p3.pressed.connect(self.runner_p3.resume)
            self.pushButton_kill_p3.pressed.connect(self.runner_p3.kill)
            self.runner_p3.signal.progress.connect(self.update_progress_p3)
            
            self.signal_p4 = WorkerSignals()
            self.runner_p4 = JobRunner(self.task_list[3], self.signal_p4, self.label_status_4)
            self.pushButton_pause_p4.pressed.connect(self.runner_p4.pause)
            self.pushButton_resume_p4.pressed.connect(self.runner_p4.resume)
            self.pushButton_kill_p4.pressed.connect(self.runner_p4.kill)
            self.runner_p4.signal.progress.connect(self.update_progress_p4)

            self.threadpool.start(self.runner_p1)
            self.label_status_1.setText(f'Corriendo')
            self.threadpool.start(self.runner_p2)
            self.label_status_2.setText(f'Corriendo')
            self.threadpool.start(self.runner_p3)
            self.label_status_3.setText(f'Corriendo')
            self.threadpool.start(self.runner_p4)
            self.label_status_4.setText(f'Corriendo')
            
            return
        
        QMessageBox.warning(self.container, 'Cuidado', 'Asigne procesos primero')
    
    def update_progress_p1(self, n):
        self.progressBar_p1.setValue(n)
    
    def update_progress_p2(self, n):
        self.progressBar_p2.setValue(n)

    def update_progress_p3(self, n):
        self.progressBar_p3.setValue(n)
    
    def update_progress_p4(self, n):
        self.progressBar_p4.setValue(n)
