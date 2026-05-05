from pyproct.driver.scheduling.task import Task


class SerialScheduler(object):
    """
    Serial scheduler compatible with the original pyscheduler implementation.
    """

    def __init__(self, functions=None):
        self.functions = functions or {}
        self.tasks = {}
        self.dependencies = {}
        self.not_completed = []
        self.finished = []
        self.results = []

    def function_exec(self, function_type, info=None):
        if function_type in self.functions:
            self.functions[function_type]['kwargs']['info'] = info
            self.functions[function_type]['function'](**(self.functions[function_type]['kwargs']))

    def run(self):
        """
        Runs all tasks once their dependencies are fulfilled.
        """
        self.function_exec('scheduling_started', {"number_of_tasks": len(self.not_completed)})

        ordered_tasks = self.get_ordered_tasks()

        for task in ordered_tasks:
            self.function_exec('task_started', {"task_name": task.name})
            self.results.append(task.run())
            self.function_exec('task_ended', {"task_name": task.name, "finished": len(self.finished)})

        self.function_exec('scheduling_ended')

        return self.results

    def get_ordered_tasks(self):
        ordered_tasks = []
        while len(self.not_completed) > 0:
            task_name = self.choose_runnable_task()

            if task_name is None:
                print("It was impossible to pick a suitable task for running. Check dependencies.")
                return []
            else:
                ordered_tasks.append(self.tasks[task_name])
                self.lock_task(task_name)
                self.complete_task(task_name)
                self.remove_from_dependencies(task_name)
        return ordered_tasks

    def choose_runnable_task(self):
        for task_name in self.not_completed:
            if len(self.dependencies[task_name]) == 0:
                return task_name
        return None

    def lock_task(self, task_name):
        self.not_completed.remove(task_name)

    def complete_task(self, task_name):
        self.finished.append(task_name)

    def remove_from_dependencies(self, task_name):
        for tn in self.dependencies:
            if task_name in self.dependencies[tn]:
                self.dependencies[tn].remove(task_name)

    def add_task(self, task_name, dependencies=None, target_function=None,
                 function_kwargs=None, description=None):
        """
        Adds a task to be executed later by run().
        """
        if dependencies is None:
            dependencies = {}
        if function_kwargs is None:
            function_kwargs = {}

        if task_name not in self.tasks:
            task = Task(name=task_name,
                        description=description,
                        function=target_function,
                        kwargs=function_kwargs)
            self.tasks[task_name] = task
            self.not_completed.append(task_name)
            self.dependencies[task_name] = dependencies
        else:
            print("[Error SerialScheduler::add_task] Task %s already exists. Task name must be unique." % task_name)
            exit()
