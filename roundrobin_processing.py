import sys
from random import randint
from time import sleep

from PySide6.QtCore import QThreadPool, QRunnable, QObject, Slot, Signal
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout,
                               QVBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox)

from task import Task


class SignalProgress(QObject):
    """ Custom signals for our progress bars """
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
        self.quantum = 3
        self.is_my_turn = False

    @Slot()
    def run(self):
        """ Run the animations """
        # This checks if the other tasks did not start yet
        if not self.is_finished and self.is_my_turn:
            # print(f'p{self.task.id_task} 1st check')
            self.status.setText('En Ejecucion')

        current_time = 0

        if self.is_my_turn and self.is_finished:
            self.signal.finished.emit()

        while self.is_my_turn and not self.is_finished:
            # Send current progress of the bar
            # print(f'p{self.task.id_task} update progress and sleep, et{self.task.elapsed_time}, ct{current_time}')
            self.signal.progress.emit(
                int((self.task.elapsed_time * 100) / self.task.execution_time))
            self.task.elapsed_time += 1
            current_time += 1
            sleep(1)

            if current_time == self.quantum:
                # print(f'p{self.task.id_task} quantom expired')
                self.status.setText('Bloqueado')
                self.is_my_turn = False
                self.signal.finished.emit()
                break

            # Infine loop for pause
            while self.is_paused:
                sleep(0)

            if self.is_finished:
                break

            if self.task.elapsed_time >= self.task.execution_time:
                # print(f'p{self.task.id_task} finish all, et{self.task.elapsed_time}')
                self.is_finished = True
                self.signal.progress.emit(100)
                self.status.setText('Terminado')
                self.signal.finished.emit()

    def pause(self):
        """ Pause the progression of the bar """
        if not self.is_finished:
            self.is_paused = True
            # Same check for the start
            if self.task.elapsed_time != 0:
                self.status.setText('Bloqueado')

    def resume(self):
        """ Resume the progression of the bar """
        if not self.is_finished:
            self.is_paused = False
            # Same check for the start
            if self.task.elapsed_time != 0:
                self.status.setText('En Ejecucion')

    def finish(self):
        """ Break the progression of the bar """
        self.is_finished = True
        self.status.setText('Terminado')
        self.signal.finished.emit()


class RRMainWindow(QMainWindow):
    """ Program that simulates RR algorithm for processing """

    def __init__(self):
        # Window configs
        super().__init__()
        self.setWindowTitle('RR Manager')
        self.resize(600, 400)

        # Vars
        self.task_list = []
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(5)

        # Left Widgets
        # We make agrupations for all the widgets to have better control, making a QGridLayout for each one

        #Label 1, presentation
        Quantum = QWidget()
        layout_q = QGridLayout(Quantum)
        label_Quantum = QLabel('Algoritmo de planificacion Round Robin\n\nQuantum 3s')
        layout_q.addWidget(label_Quantum, 0, 0)

        # Proccess 01 Set
        container_p1 = QWidget()
        layout_p1 = QGridLayout(container_p1)

        label_title_p1 = QLabel('Proceso 01')
        self.label_state_p1 = QLabel('Nuevo')
        self.label_time_p1 = QLabel('0s')
        self.progress_bar_p1 = QProgressBar()

        layout_p1.addWidget(label_title_p1, 0, 0)
        layout_p1.addWidget(self.label_state_p1, 0, 1)
        layout_p1.addWidget(self.label_time_p1, 0, 2)
        layout_p1.addWidget(self.progress_bar_p1, 1, 0, -1, -1)

        # Proccess 02 Set
        container_p2 = QWidget()
        layout_p2 = QGridLayout(container_p2)

        label_title_p2 = QLabel('Proceso 02')
        self.label_state_p2 = QLabel('Nuevo')
        self.label_time_p2 = QLabel('0s')
        self.progress_bar_p2 = QProgressBar()

        layout_p2.addWidget(label_title_p2, 0, 0)
        layout_p2.addWidget(self.label_state_p2, 0, 1)
        layout_p2.addWidget(self.label_time_p2, 0, 2)
        layout_p2.addWidget(self.progress_bar_p2, 1, 0, -1, -1)

        # Proccess 03 Set
        container_p3 = QWidget()
        layout_p3 = QGridLayout(container_p3)

        label_title_p3 = QLabel('Proceso 03')
        self.label_state_p3 = QLabel('Nuevo')
        self.label_time_p3 = QLabel('0s')
        self.progress_bar_p3 = QProgressBar()

        layout_p3.addWidget(label_title_p3, 0, 0)
        layout_p3.addWidget(self.label_state_p3, 0, 1)
        layout_p3.addWidget(self.label_time_p3, 0, 2)
        layout_p3.addWidget(self.progress_bar_p3, 1, 0, -1, -1)

        # Proccess 04 Set
        container_p4 = QWidget()
        layout_p4 = QGridLayout(container_p4)

        label_title_p4 = QLabel('Proceso 04')
        self.label_state_p4 = QLabel('Nuevo')
        self.label_time_p4 = QLabel('0s')
        self.progress_bar_p4 = QProgressBar()

        layout_p4.addWidget(label_title_p4, 0, 0)
        layout_p4.addWidget(self.label_state_p4, 0, 1)
        layout_p4.addWidget(self.label_time_p4, 0, 2)
        layout_p4.addWidget(self.progress_bar_p4, 1, 0, -1, -1)

        # Right Widgets
        # Buttons
        self.button_resume = QPushButton('Continuar')
        self.button_pause = QPushButton('Pausar')
        self.button_finish = QPushButton('Terminar')
        self.button_assign = QPushButton('Asignar Procesos')
        self.button_execute = QPushButton('Ejecutar')

        self.button_assign.clicked.connect(self.assign_tasks)  # type: ignore
        self.button_execute.clicked.connect(self.start_execution)  # type: ignore

        # Main Layouts
        # This way we put all layouts and set the widgets on the window
        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QGridLayout()
        layout_right.setSpacing(10)

        layout_main.addLayout(layout_left)
        layout_main.addLayout(layout_right)
        layout_left.addWidget(Quantum)
        layout_left.addWidget(container_p1)
        layout_left.addWidget(container_p2)
        layout_left.addWidget(container_p3)
        layout_left.addWidget(container_p4)

        layout_right.addWidget(self.button_resume, 0, 0)
        layout_right.addWidget(self.button_pause, 0, 1)
        layout_right.addWidget(self.button_finish, 0, 2)
        layout_right.addWidget(self.button_assign, 1, 0, 1, 1)
        layout_right.addWidget(self.button_execute, 1, 1, 1, 2)

        self.container = QWidget()
        self.container.setLayout(layout_main)
        self.setCentralWidget(self.container)
    # __init__

    def assign_tasks(self):
        """ Create tasks with random times, append to the list and update """
        # Clear the list for assign new tasks
        self.task_list.clear()

        # Create new tasks, then update the program
        for i in range(4):
            time = randint(3, 15)
            task = Task(i+1, time, 0, time)
            self.task_list.append(task)

        self.label_state_p1.setText('Listo')
        self.label_state_p2.setText('Listo')
        self.label_state_p3.setText('Listo')
        self.label_state_p4.setText('Listo')

        self.label_time_p1.setText(f'{self.task_list[0].execution_time}s')
        self.label_time_p2.setText(f'{self.task_list[1].execution_time}s')
        self.label_time_p3.setText(f'{self.task_list[2].execution_time}s')
        self.label_time_p4.setText(f'{self.task_list[3].execution_time}s')

        self.progress_bar_p1.setValue(0)
        self.progress_bar_p2.setValue(0)
        self.progress_bar_p3.setValue(0)
        self.progress_bar_p4.setValue(0)

        # Make available another run of the program
        self.button_execute.setDisabled(False)
    # assing_tasks

    def start_execution(self):
        """ Set all bars threads and signals """
        if self.task_list:
            self.signal_p1 = SignalProgress()
            self.thread_p1 = RunProgress(self.task_list[0], self.label_state_p1, self.signal_p1)
            self.thread_p1.signal.progress.connect(self.update_progress_p1)
            self.thread_p1.signal.finished.connect(self.finish_p1)

            self.signal_p2 = SignalProgress()
            self.thread_p2 = RunProgress(self.task_list[1], self.label_state_p2, self.signal_p2)
            self.thread_p2.signal.progress.connect(self.update_progress_p2)
            self.thread_p2.signal.finished.connect(self.finish_p2)

            self.signal_p3 = SignalProgress()
            self.thread_p3 = RunProgress(self.task_list[2], self.label_state_p3, self.signal_p3)
            self.thread_p3.signal.progress.connect(self.update_progress_p3)
            self.thread_p3.signal.finished.connect(self.finish_p3)

            self.signal_p4 = SignalProgress()
            self.thread_p4 = RunProgress(self.task_list[3], self.label_state_p4, self.signal_p4)
            self.thread_p4.signal.progress.connect(self.update_progress_p4)
            self.thread_p4.signal.finished.connect(self.finish_p4)

            # Same signals for all tasks (1 button for all)
            self.button_resume.pressed.connect(self.thread_p1.resume)  # type: ignore
            self.button_resume.pressed.connect(self.thread_p2.resume)  # type: ignore
            self.button_resume.pressed.connect(self.thread_p3.resume)  # type: ignore
            self.button_resume.pressed.connect(self.thread_p4.resume)  # type: ignore

            self.button_pause.pressed.connect(self.thread_p1.pause)  # type: ignore
            self.button_pause.pressed.connect(self.thread_p2.pause)  # type: ignore
            self.button_pause.pressed.connect(self.thread_p3.pause)  # type: ignore
            self.button_pause.pressed.connect(self.thread_p4.pause)  # type: ignore

            self.button_finish.pressed.connect(self.thread_p1.finish)  # type: ignore
            self.button_finish.pressed.connect(self.thread_p2.finish)  # type: ignore
            self.button_finish.pressed.connect(self.thread_p3.finish)  # type: ignore
            self.button_finish.pressed.connect(self.thread_p4.finish)  # type: ignore

            self.thread_p1.is_my_turn = True
            self.thread_pool.start(self.thread_p1)
            self.thread_pool.start(self.thread_p2)
            self.thread_pool.start(self.thread_p3)
            self.thread_pool.start(self.thread_p4)

            # TODO
            # Disable the other buttons, freezing gui
            # Disable buttons while running
            self.button_assign.setDisabled(True)
            self.button_execute.setDisabled(True)
            
            return

        QMessageBox.warning(self.container, 'Cuidado','Asigne procesos primero')
    # start_execution

    # This slots pass the turn to the next task until all are finished
    def finish_p1(self):
        self.thread_p2.is_my_turn = True
        self.thread_p2.run()

    def finish_p2(self):
        self.thread_p3.is_my_turn = True
        self.thread_p3.run()

    def finish_p3(self):
        self.thread_p4.is_my_turn = True
        self.thread_p4.run()

    def finish_p4(self):
        # If all tasks are finished, stop the program
        if self.all_finish():
            QMessageBox.information(self.container, 'Ejecucion Terminada', 'El Lote termino de ejecutarse')
            self.button_assign.setDisabled(False)
            return

        self.thread_p1.is_my_turn = True
        self.thread_p1.run()

    def all_finish(self):
        """ Check if all tasks are finished """
        if (self.thread_p1.is_finished and self.thread_p2.is_finished and
                self.thread_p3.is_finished and self.thread_p4.is_finished):
            return True
        return False

    # Update signals, set the values in the bars
    def update_progress_p1(self, n):
        self.progress_bar_p1.setValue(n)

    def update_progress_p2(self, n):
        self.progress_bar_p2.setValue(n)

    def update_progress_p3(self, n):
        self.progress_bar_p3.setValue(n)

    def update_progress_p4(self, n):
        self.progress_bar_p4.setValue(n)


if __name__ == '__main__':
    # Start the program
    app = QApplication()
    window = RRMainWindow()
    window.show()
    sys.exit(app.exec())
