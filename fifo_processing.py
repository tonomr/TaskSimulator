import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QProgressBar


class FIFOMainWindow(QMainWindow):
    """ Program that simulates FIFO algorithm for processing """
    def __init__(self):
        # Window configs
        super().__init__()
        self.setWindowTitle('FIFO Manager')
        self.resize(600, 400)

        ### Left Widgets
        ## We make agrupations for all the widgets to have better control, making a QGridLayout for each one
        # Proccess 01 Set
        container_p1 = QWidget()
        layout_p1 = QGridLayout(container_p1)

        label_title_p1 = QLabel('Proceso 01')
        label_state_p1 = QLabel('Nuevo')
        label_time_p1 = QLabel('0s')
        progress_bar_p1 = QProgressBar()

        layout_p1.addWidget(label_title_p1, 0, 0)
        layout_p1.addWidget(label_state_p1, 0, 1)
        layout_p1.addWidget(label_time_p1, 0, 2)
        layout_p1.addWidget(progress_bar_p1, 1, 0, -1, -1)

        # Proccess 02 Set
        container_p2 = QWidget()
        layout_p2 = QGridLayout(container_p2)

        label_title_p2 = QLabel('Proceso 02')
        label_state_p2 = QLabel('Nuevo')
        label_time_p2 = QLabel('0s')
        progress_bar_p2 = QProgressBar()

        layout_p2.addWidget(label_title_p2, 0, 0)
        layout_p2.addWidget(label_state_p2, 0, 1)
        layout_p2.addWidget(label_time_p2, 0, 2)
        layout_p2.addWidget(progress_bar_p2, 1, 0, -1, -1)

        # Proccess 03 Set
        container_p3 = QWidget()
        layout_p3 = QGridLayout(container_p3)

        label_title_p3 = QLabel('Proceso 03')
        label_state_p3 = QLabel('Nuevo')
        label_time_p3 = QLabel('0s')
        progress_bar_p3 = QProgressBar()

        layout_p3.addWidget(label_title_p3, 0, 0)
        layout_p3.addWidget(label_state_p3, 0, 1)
        layout_p3.addWidget(label_time_p3, 0, 2)
        layout_p3.addWidget(progress_bar_p3, 1, 0, -1, -1)

        # Proccess 04 Set
        container_p4 = QWidget()
        layout_p4 = QGridLayout(container_p4)

        label_title_p4 = QLabel('Proceso 04')
        label_state_p4 = QLabel('Nuevo')
        label_time_p4 = QLabel('0s')
        progress_bar_p4 = QProgressBar()

        layout_p4.addWidget(label_title_p4, 0, 0)
        layout_p4.addWidget(label_state_p4, 0, 1)
        layout_p4.addWidget(label_time_p4, 0, 2)
        layout_p4.addWidget(progress_bar_p4, 1, 0, -1, -1)

        ### Right Widgets
        # Buttons
        button_execution = QPushButton('Ejecutar')
        button_pause = QPushButton('Pausar')
        button_finish = QPushButton('Terminar')

        ### Main Layouts
        ## This way we put all layouts and set the widgets on the window
        layout_main = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QHBoxLayout()

        layout_main.addLayout(layout_left)
        layout_main.addLayout(layout_right)

        layout_left.addWidget(container_p1)
        layout_left.addWidget(container_p2)
        layout_left.addWidget(container_p3)
        layout_left.addWidget(container_p4)

        layout_right.addWidget(button_execution)
        layout_right.addWidget(button_pause)
        layout_right.addWidget(button_finish)

        container = QWidget()
        container.setLayout(layout_main)
        self.setCentralWidget(container)


if __name__ == '__main__':
    ### Start the program
    app = QApplication()
    window = FIFOMainWindow()
    window.show()
    sys.exit(app.exec())
