from dataclasses import dataclass


@dataclass
class Task:
    """Data class of Task"""
    _id_task: int
    _execution_time: int
    _elapsed_time: int
    _remaining_time: int
    _priority: int = -1

    @property
    def id_task(self) -> int:
        return self._id_task

    @id_task.setter
    def id_task(self, v: int) -> None:
        self._id_task = v

    @property
    def execution_time(self) -> int:
        return self._execution_time

    @execution_time.setter
    def execution_time(self, v: int) -> None:
        self._execution_time = v

    @property
    def elapsed_time(self) -> int:
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, v: int) -> None:
        self._elapsed_time = v

    @property
    def remaining_time(self) -> int:
        return self._remaining_time

    @remaining_time.setter
    def remaining_time(self, v: int) -> None:
        self._remaining_time = v
    
    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, v: int) -> None:
        self._priority = v


if __name__ == '__main__':
    task = Task(1, 8, 1, 7)
    print(task)
