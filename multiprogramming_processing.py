import sys
from random import randint
from time import sleep

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, \
    QProgressBar, QMessageBox

from task import Task


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Procesamiento con Multiprogramacion')
        self.resize(600, 400)

        self.task_list = []

        label_title = QLabel('Procesos a ejecutar')
        label_title.setAlignment(Qt.AlignCenter)

        self.label_1 = QLabel('Proceso #1, tiempo 0s')
        self.bar_progress_1 = QProgressBar()
        self.label_2 = QLabel('Proceso #2, tiempo 0s')
        self.bar_progress_2 = QProgressBar()
        self.label_3 = QLabel('Proceso #3, tiempo 0s')
        self.bar_progress_3 = QProgressBar()
        self.label_4 = QLabel('Proceso #4, tiempo 0s')
        self.bar_progress_4 = QProgressBar()

        self.button_assign = QPushButton('Asignar procesos')
        self.button_assign.clicked.connect(self.asign_tasks)
        self.button_start = QPushButton('Empezar procesamiento')
        self.button_start.clicked.connect(self.start_execution)

        # Layouts
        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        layout_main.addLayout(layout_left)
        layout_main.addLayout(layout_right)

        layout_left.addWidget(label_title)
        layout_left.addWidget(self.label_1)
        layout_left.addWidget(self.bar_progress_1)
        layout_left.addWidget(self.label_2)
        layout_left.addWidget(self.bar_progress_2)
        layout_left.addWidget(self.label_3)
        layout_left.addWidget(self.bar_progress_3)
        layout_left.addWidget(self.label_4)
        layout_left.addWidget(self.bar_progress_4)

        layout_right.addWidget(self.button_assign)
        layout_right.addWidget(self.button_start)

        # Set main layout
        container = QWidget()
        container.setLayout(layout_main)
        self.setCentralWidget(container)

    def asign_tasks(self):
        # Fill the task list
        for i in range(4):
            exec_time = randint(2, 16)
            task = Task(i + 1, exec_time, 0, exec_time)
            self.task_list.append(task)

        self.label_1.setText(
            f'Proceso #1, tiempo {self.task_list[0].execution_time}s')
        self.label_2.setText(
            f'Proceso #2, tiempo {self.task_list[1].execution_time}s')
        self.label_3.setText(
            f'Proceso #3, tiempo {self.task_list[2].execution_time}s')
        self.label_4.setText(
            f'Proceso #4, tiempo {self.task_list[3].execution_time}s')

    def start_execution(self):
        if self.task_list:
            self.button_assign.setEnabled(False)
            self.button_start.setEnabled(False)
            self.worker = WorkerThread(self.max_execution_time(), self.task_list)
            self.worker.start()
            self.worker.update_progress_1.connect(self.event_worker_update_1)
            self.worker.update_progress_2.connect(self.event_worker_update_2)
            self.worker.update_progress_3.connect(self.event_worker_update_3)
            self.worker.update_progress_4.connect(self.event_worker_update_4)
            self.worker.finished.connect(self.event_worker_finish)
            return

        QMessageBox.warning(self, 'Cuidado', 'Asigne procesos primero')

    def event_worker_update_1(self, value):
        """Update the bar"""
        self.bar_progress_1.setValue(value)
        if value >= 100:
            self.label_1.setText(f'Proceso #1, con duracion de {self.task_list[0].execution_time}s: FINALIZADO')

    def event_worker_update_2(self, value):
        """Update the bar"""
        self.bar_progress_2.setValue(value)
        if value>=100:
            self.label_2.setText(f'Proceso #2, con duracion de {self.task_list[1].execution_time}s: FINALIZADO')

    def event_worker_update_3(self, value):
        """Update the bar"""
        self.bar_progress_3.setValue(value)
        if value>=100:
            self.label_3.setText(f'Proceso #3, con duracion de {self.task_list[2].execution_time}s: FINALIZADO')

    def event_worker_update_4(self, value):
        """Update the bar"""
        self.bar_progress_4.setValue(value)
        if value>=100:
            self.label_4.setText(f'Proceso #4, con duracion de {self.task_list[3].execution_time}s: FINALIZADO')

    def event_worker_finish(self):
        """Clean tasks list"""
        self.task_list.clear()
        QMessageBox.information(
            self, 'Procesos terminados', 'Se ha terminado de ejecutar los procesos :)')

        self.bar_progress_1.setValue(0)
        self.bar_progress_2.setValue(0)
        self.bar_progress_3.setValue(0)
        self.bar_progress_4.setValue(0)

        self.button_assign.setEnabled(True)
        self.button_start.setEnabled(True)

    def max_execution_time(self) -> int:
        max_exec_time = 0
        for i in range(4):
            if self.task_list[i].execution_time > max_exec_time:
                max_exec_time = self.task_list[i].execution_time
        return max_exec_time


class WorkerThread(QThread):
    def __init__(self, max_time, tasks):
        super().__init__()
        self.max_time = max_time
        self.tasks = tasks

    update_progress_1 = Signal(int)
    update_progress_2 = Signal(int)
    update_progress_3 = Signal(int)
    update_progress_4 = Signal(int)

    def run(self):
        for s in range(self.max_time + 1):
            self.update_progress_1.emit(
                int((self.tasks[0].elapsed_time * 100) / self.tasks[0].execution_time))
            self.update_progress_2.emit(
                int((self.tasks[1].elapsed_time * 100) / self.tasks[1].execution_time))
            self.update_progress_3.emit(
                int((self.tasks[2].elapsed_time * 100) / self.tasks[2].execution_time))
            self.update_progress_4.emit(
                int((self.tasks[3].elapsed_time * 100) / self.tasks[3].execution_time))

            self.tasks[0].elapsed_time += 1
            self.tasks[1].elapsed_time += 1
            self.tasks[2].elapsed_time += 1
            self.tasks[3].elapsed_time += 1

            sleep(1)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
