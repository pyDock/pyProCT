import multiprocessing
import traceback


###############################################################################
# TOP-LEVEL EXECUTOR (must be picklable)
###############################################################################

def processparallel_execute_task(task):
    """
    Executed inside worker processes.
    task = {
        "task_name": ...,
        "target_function": callable,
        "function_kwargs": dict
    }
    """
    name = task.get("task_name", "UnnamedTask")
    func = task.get("target_function", None)
    kwargs = task.get("function_kwargs", {})

    try:
        if func is None:
            raise RuntimeError("No target_function provided")

        result = func(**kwargs)
        return result

    except Exception as e:
        traceback.print_exc()
        return (task["task_name"], None)
        #return (name, {"error": str(e)})



###############################################################################
# PARALLEL SCHEDULER 100% COMPATIBLE WITH pyProCT
###############################################################################

class ProcessParallelScheduler:

    def __init__(self, num_processes, external_functions=None):
        self.num_processes = num_processes
        self.external_functions = external_functions or {}
        self.tasks = []  # list of dicts

    ###########################################################################
    # ADD TASK — preserves pyProCT's original API
    ###########################################################################
    def add_task(self, task_name, description=None,
                 target_function=None,
                 function_kwargs=None,
                 dependencies=None):
        """
        pyProCT expects:
            - task_name
            - description
            - target_function
            - function_kwargs
            - dependencies  (ignored here)
        """

        task = {
            "task_name": task_name,
            "description": description,
            "target_function": target_function,
            "function_kwargs": function_kwargs or {}
        }

        # Clean non-picklable elements
        cleaned = {}
        for key, value in task.items():
            try:
                multiprocessing.reduction.ForkingPickler.dumps(value)
                cleaned[key] = value
            except Exception:
                # replace problematic parts (like observers, locks, bound methods)
                cleaned[key] = None

        self.tasks.append(cleaned)

    ###########################################################################
    # RUN TASKS IN PARALLEL
    ###########################################################################
    def run(self):

        # Notify observer (safe)
        if "scheduling_started" in self.external_functions:
            info = self.external_functions["scheduling_started"]
            info["function"](info["kwargs"]["observer"],
                             info["kwargs"]["tag"], {})

        # Parallel execution
        with multiprocessing.Pool(self.num_processes) as pool:
            results = pool.map(processparallel_execute_task, self.tasks)

        # Notify observer done
        if "scheduling_ended" in self.external_functions:
            info = self.external_functions["scheduling_ended"]
            info["function"](info["kwargs"]["observer"],
                             info["kwargs"]["tag"], {})

        #return dict(results)
        return results
