class Task:
    """Data class of Task"""

    def __init__(self, id_task, execution_time=0, elapsed_time=0, remaining_time=0):
        self._id_task = id_task
        self._execution_time = execution_time
        self._elapsed_time = elapsed_time
        self._remaining_time = remaining_time

    def __str__(self):
        return f'Task #{self._id_task}:\n' \
               f'Execution time: {self._execution_time}s\n' \
               f'Elapsed time: {self._elapsed_time}s\n' \
               f'Remaining time: {self._remaining_time}s'

    def get_id_task(self):
        return self._id_task

    def get_execution_time(self):
        return self._execution_time

    def get_elapsed_time(self):
        return self._elapsed_time

    def get_remaining_time(self):
        return self._remaining_time

    def set_id_task(self, id_task):
        self._id_task = id_task

    def set_execution_time(self, execution_time):
        self._execution_time = execution_time

    def set_elapsed_time(self, elapsed_time):
        self._elapsed_time = elapsed_time

    def set_remaining_time(self, remaining_time):
        self._remaining_time = remaining_time

# Test class object
if __name__ == '__main__':
    task1 = Task(0, 10, 2, 8)
    print(task1)
