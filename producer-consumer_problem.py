import sys
from time import sleep

from PySide6.QtCore import (
    QCoreApplication, QMetaObject, Qt, QObject, QRunnable, QThreadPool, Signal, Slot)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout,
                               QLabel, QMainWindow, QProgressBar, QPushButton, QWidget, QMessageBox)


class SignalProgress(QObject):
    progress = Signal(int)


class RunProgress(QRunnable):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    @Slot()
    def run(self):
        for s in range(10):
            print(f'Here we are {s}s')
            sleep(1.0)


class ProducerConsumerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        """ Create the widgets to setup the window """
        # Window configuration
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)

        # Layout
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        # Vars
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(4)

        # Labels
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setFrameShape(QFrame.Box)
        self.label_title.setFrameShadow(QFrame.Plain)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_title, 0, 0, 1, 3)

        self.label_producer = QLabel(self.centralwidget)
        self.label_producer.setObjectName(u"label_producer")
        self.label_producer.setAlignment(Qt.AlignCenter)
        self.label_producer.setWordWrap(True)
        self.gridLayout.addWidget(self.label_producer, 1, 0, 1, 1)

        self.label_consumer = QLabel(self.centralwidget)
        self.label_consumer.setObjectName(u"label_consumer")
        self.label_consumer.setAlignment(Qt.AlignCenter)
        self.label_consumer.setWordWrap(True)
        self.gridLayout.addWidget(self.label_consumer, 1, 2, 1, 1)

        self.label_status = QLabel(self.centralwidget)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_status, 4, 1, 1, 1)

        # Buttons
        self.pushButton_producer = QPushButton(self.centralwidget)
        self.pushButton_producer.setObjectName(u"pushButton_producer")
        self.gridLayout.addWidget(self.pushButton_producer, 2, 0, 1, 1)
        self.pushButton_producer.clicked.connect(self.run_producer)

        self.pushButton_stop_producer = QPushButton(self.centralwidget)
        self.pushButton_stop_producer.setObjectName(
            u"pushButton_stop_producer")
        self.gridLayout.addWidget(self.pushButton_stop_producer, 3, 0, 1, 1)
        self.pushButton_stop_producer.clicked.connect(self.stop_producer)

        self.pushButton_consumer = QPushButton(self.centralwidget)
        self.pushButton_consumer.setObjectName(u"pushButton_consumer")
        self.gridLayout.addWidget(self.pushButton_consumer, 2, 2, 1, 1)
        self.pushButton_consumer.clicked.connect(self.run_consumer)

        self.pushButton_stop_consumer = QPushButton(self.centralwidget)
        self.pushButton_stop_consumer.setObjectName(
            u"pushButton_stop_consumer")
        self.gridLayout.addWidget(self.pushButton_stop_consumer, 3, 2, 1, 1)
        self.pushButton_stop_consumer.clicked.connect(self.stop_consumer)

        # ProgressBar
        self.progressBar_buffer = QProgressBar(self.centralwidget)
        self.progressBar_buffer.setObjectName(u"progressBar_buffer")
        self.progressBar_buffer.setValue(50)
        self.gridLayout.addWidget(self.progressBar_buffer, 5, 0, 1, 3)

        # Set all widgets in the window
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Producer-Consumer problem", None))
        self.label_consumer.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso Consumidor", None))
        self.label_status.setText(QCoreApplication.translate(
            "MainWindow", u"Inactivo", None))
        self.label_title.setText(QCoreApplication.translate(
            "MainWindow", u"El Problema del Productor-Consumidor", None))
        self.pushButton_producer.setText(
            QCoreApplication.translate("MainWindow", u"Producir", None))
        self.pushButton_consumer.setText(
            QCoreApplication.translate("MainWindow", u"Consumir", None))
        self.label_producer.setText(QCoreApplication.translate(
            "MainWindow", u"Proceso Productor", None))
        self.progressBar_buffer.setFormat(
            QCoreApplication.translate("MainWindow", u"%p", None))
        self.pushButton_stop_consumer.setText(
            QCoreApplication.translate("MainWindow", u"Detener", None))
        self.pushButton_stop_producer.setText(
            QCoreApplication.translate("MainWindow", u"Detener", None))
    # retranslateUi

    def run_producer(self):
        print("Running producer!")
        self.s1 = SignalProgress()
        self.t1 = RunProgress(self.s1)
        self.thread_pool.start(self.t1)
    # run_consumer

    def stop_producer(self):
        print("Stopping producer!")
    # stop_producer

    def run_consumer(self):
        print("Running consumer!")
    # run_consumer

    def stop_consumer(self):
        print("Stopping consumer!")
    # stop_consumer


if __name__ == "__main__":
    app = QApplication([])
    window = ProducerConsumerWindow()
    window.show()
    sys.exit(app.exec())
