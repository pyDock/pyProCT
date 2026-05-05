class WorkerError:
    """Wrapper for an error raised inside a worker."""
    def __init__(self, message, trace):
        self.message = message
        self.trace = trace

    def __str__(self):
        return f"[WorkerError] {self.message}\n{self.trace}"


class Task:
    """
    Generic task compatible with the original pyscheduler Task contract.
    """

    def __init__(self, name, description, function, kwargs=None):
        self.name = name
        self.description = description
        self.function = function
        self.kwargs = kwargs or {}
        self.result = None

    def run(self):
        """Executes the task target function."""
        self.result = self.function(**self.kwargs)
        return self.result
