class SerialScheduler:
    def __init__(self, external_functions):
        """
        external_functions = {
            task_started: {...},
            task_ended: {...},
            scheduling_started: {...},
            scheduling_ended: {...}
        }
        """
        self.external = external_functions

    def _callback(self, key, info=None):
        fn = self.external[key]["function"]
        kwargs = self.external[key]["kwargs"]
        fn(info, **kwargs)

    def run(self, tasks):
        self._callback("scheduling_started")

        results = []
        for t in tasks:
            self._callback("task_started", t.task_info)
            try:
                r = t.run()
            except Exception as e:
                r = e
            results.append(r)
            self._callback("task_ended", t.task_info)

        self._callback("scheduling_ended")
        return results

