import tkinter as tk
from tkinter import ttk
from time import sleep
from random import randint
from threading import Thread
from task import Task


class MainWindow(tk.Tk):
    '''Main Window for our GUI'''

    def __init__(self):
        super().__init__()

        # Main configuration
        self.title('Procesamiento por Lotes')
        self.geometry('600x400')
        self.resizable(False, False)

        # Grid configuration
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)

        # Class components and vars
        self._id_counter = 0
        self._task_list = []
        self._frame_list = tk.Frame(self)
        self._list_box_task = tk.Listbox(self._frame_list, width=25)
        self._scroll_bar = tk.Scrollbar(
            self._frame_list, orient='vertical', command=self._list_box_task.yview)

        self._create_components()

    def _create_random_task(self):
        """Create a task with random values and add it to the list and GUI"""
        exec_time = randint(2, 10)
        task = Task(self._id_counter, exec_time, 0, exec_time)
        self._id_counter += 1

        self._task_list.append(task)
        self._list_box_task.insert(
            tk.END, f'Proceso #{task.get_id_task()},  Tiempo: {task.get_execution_time()}s')

    def _run_tasks(self, label, task_window):
        task_progress = ttk.Progressbar(
            task_window, orient='horizontal', length=200)
        task_progress.pack()

        # Update the bar and the current task
        for task in self._task_list:
            label.configure(text=f'Proceso #{task.get_id_task()}')

            threadUpdate = Thread(
                target=self._update_elapsed, args=(task, task_progress,))
            threadUpdate.start()

            sleep(task.get_execution_time())

        # Close execution window and clean the list
        task_window.destroy()
        self._task_list.clear()
        self._list_box_task.delete(0, tk.END)

    def _update_elapsed(self, task, bar):
        total_time = task.get_execution_time()
        current_time = 1

        while True:
            bar['maximum'] = 100

            currentV = task.get_elapsed_time()

            # Get the progress second of the actual task and update the bar
            calculatedValue = int((currentV * bar['maximum']) / total_time)
            # print(calculatedValue, currentV, bar['maximum'])
            bar["value"] = calculatedValue
            bar.update()

            if current_time >= total_time:
                break

            current_time += 1
            task.set_elapsed_time(current_time)
            task.set_remaining_time(task.get_remaining_time()-1)

            sleep(1)

    def _start_execution(self):
        task_window = tk.Toplevel()
        task_window.geometry('300x200')
        task_window.title('Ejecutando procesos')

        label_task = tk.Label(task_window, text='Proceso #0')
        label_task.pack()

        # Threading for display the window and start the execution of tasks
        t1 = Thread(target=self._run_tasks, args=(label_task, task_window,))
        t1.start()

    def _create_components(self):
        label_title = ttk.Label(self, text='Lista de Procesos')
        label_title.grid(row=0, column=0, pady=20)

        self._frame_list.grid(row=1, column=0, rowspan=3)
        self._list_box_task.grid(row=0, column=0, sticky='NSEW')
        self._scroll_bar.grid(row=0, column=1, sticky='NS')
        self._list_box_task.configure(yscrollcommand=self._scroll_bar.set)

        button_random = ttk.Button(
            self, text='Agregar proceso aleatorio', command=self._create_random_task)
        button_random.grid(row=1, column=1)

        # button_new = ttk.Button(self, text='Agregar nuevo proceso')
        # button_new.grid(row=2, column=1)

        button_start = ttk.Button(
            self, text='Empezar ejecución', command=self._start_execution)
        button_start.grid(row=3, column=1, pady=35, sticky='S')


# Run window
if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()
