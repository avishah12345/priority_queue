class PriorityQueue:
    def __init__(self):
        self._queue = list()

    def insert(self, priority: int, target, args: tuple = None, kwargs: dict = None):
        """
        :param priority: Lower the value, higher the priority
        :param target: Callable
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: None
        """
        self._queue.append((priority, target, args or tuple(), kwargs or dict()))

    def run(self, count: int = 1, priority: bool = False):
        """
        :param count: Runs first {count} functions
        :param priority: If true, runs all functions with the same and highest priority. Overrides count
        :return:
        """
        self._queue.sort()  # sorting only by first item should be faster, but for some reason isn't
        if priority:
            try: p_to_run = self._queue[0][0]
            except IndexError: return
            items = tuple(filter(lambda p: p[0] == p_to_run, self._queue))
            for _, target, args, kwargs in items:
                target(*args, **kwargs)
            del self._queue[:len(items)]
            return
        for _ in range(count):
            try: __, target, args, kwargs = self._queue.pop(0)
            except IndexError: return
            else: target(*args, **kwargs)


if __name__ == '__main__':
    import time

    start = time.perf_counter()

    queue = PriorityQueue()
    queue.insert(2, print, ("Low priority",), kwargs={'end': ' kwargs\n'})
    queue.insert(1, print, ("Medium Priority",))
    queue.run()  # till now, medium priority has highest priority, executes firsts
    queue.insert(0, print, ("High priority",))
    queue.run(3)  # now high and low priority are present in queue, higher one executes first

    queue.insert(2, print, ("Low priority",))
    queue.insert(1, print, ("\nMedium Priority 2",))
    queue.insert(2, print, ("Low priority 2",))
    queue.insert(1, print, ("Medium Priority",))
    queue.run(priority=True)
    queue.run(priority=True)
    queue.run(priority=True)

    print(f"{(time.perf_counter() - start) * 1000000} ns")
