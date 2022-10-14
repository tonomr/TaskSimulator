import sys
from random import randint
from time import sleep
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QPushButton, QProgressBar, QMessageBox

from task import Task

class ExecutionWindow(QWidget):
    """Execution window for batching"""

    def __init__(self):
        # Window configurations
        super().__init__()
        self.setWindowTitle('Ejecutando Procesos')
        self.resize(300, 200)

        # Components
        self.label_current_task = QLabel('Proceso #0')
        self.progress_bar = QProgressBar()

        # Layout
        layout_execution = QVBoxLayout()
        layout_execution.addWidget(self.label_current_task)
        layout_execution.addWidget(self.progress_bar)

        self.setLayout(layout_execution)


class MainWindow(QMainWindow):
    """Main window of app"""

    def __init__(self):
        # Window configurations
        super().__init__()
        self.setWindowTitle('Procesamiento por Lotes')
        self.resize(600, 400)

        # Class vars
        self._id_counter = 1
        self._task_list = []

        # Components
        title_label = QLabel('Lista de Procesos')
        title_label.setAlignment(Qt.AlignCenter)
        self.box_list = QListWidget()

        button_add_random_task = QPushButton('Agregar proceso aleatorio')
        button_add_random_task.clicked.connect(self._create_random_task)

        button_start = QPushButton('Empezar ejecucion')
        button_start.clicked.connect(self._start_execution)

        self.execution_window = ExecutionWindow()

        # Layouts
        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        layout_main.addLayout(layout_left)
        layout_main.addLayout(layout_right)

        layout_left.addWidget(title_label)
        layout_left.addWidget(self.box_list)
        layout_right.addWidget(button_add_random_task)
        layout_right.addWidget(button_start)

        # Set main layout
        container = QWidget()
        container.setLayout(layout_main)
        self.setCentralWidget(container)

    def _create_random_task(self) -> None:
        """Generate a random task and append to the list"""
        exec_time = randint(2, 10)
        task = Task(self._id_counter, exec_time, 0, exec_time)
        self._id_counter += 1
        self._task_list.append(task)
        self.box_list.addItem(
            f'Proceso #{task.id_task}, tiempo: {task.execution_time}s')

    def _start_execution(self) -> None:
        """Start batch processing in new window"""
        self.execution_window.show()

        self.worker = WorkerThread(
            self._task_list, self.execution_window.label_current_task)
        self.worker.start()
        self.worker.finished.connect(self.event_worker_finish)
        self.worker.update_progress.connect(self.event_worker_update)

    def event_worker_finish(self):
        """Clean tasks list"""
        self._task_list.clear()
        self.box_list.clear()
        QMessageBox.information(
            self, 'Procesos terminados', 'Se ha terminado de ejecutar los procesos :)')
        self.execution_window.hide()

    def event_worker_update(self, value):
        """Update the bar"""
        self.execution_window.progress_bar.setValue(value)


class WorkerThread(QThread):
    def __init__(self, tasks, label):
        super().__init__()
        self._tasks = tasks
        self._label = label

    update_progress = Signal(int)

    def run(self):
        for t in self._tasks:
            self._label.setText(f'Proceso #{t.id_task}')

            for s in range(t.execution_time+1):
                self.update_progress.emit(
                    int((t.elapsed_time*100) / t.execution_time))
                t.elapsed_time += 1
                t.remaining_time -= 1
                sleep(1)
            """Function that is responsible for calculating the percentage of the remaining time of the real process"""
            t.elapsed_time -= 1
            t.remaining_time += 1


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
