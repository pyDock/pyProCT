import importlib
import traceback


class WorkerError:
    """Wrapper for an error raised inside a worker."""
    def __init__(self, message, trace):
        self.message = message
        self.trace = trace

    def __str__(self):
        return f"[WorkerError] {self.message}\n{self.trace}"


class Task:
    """
    Generic serializable task used by the new scheduler.
    Stores module, class and method names so workers can import dynamically.
    """

    def __init__(self, module_name, class_name, method_name, args=None, kwargs=None, task_info=None):
        self.module_name = module_name
        self.class_name = class_name
        self.method_name = method_name
        self.args = args or []
        self.kwargs = kwargs or {}
        self.task_info = task_info or {}

    def run(self):
        """Executed inside workers."""
        module = importlib.import_module(self.module_name)
        cls = getattr(module, self.class_name)
        method = getattr(cls, self.method_name)
        return method(*self.args, **self.kwargs)

