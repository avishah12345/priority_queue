from typing import Callable


class PriorityQueue:
    def __init__(self):
        self._queue = list()

    def __repr__(self):
        self._queue.sort()

        def mapper(item):
            priority, target, args, kwargs = item
            return f"\n\t({priority=}, {target=}, {args=}, {kwargs=})"

        t = ','.join(map(mapper, self._queue))
        return f"PriorityQueue(queue=[{t}\n])"

    def insert(self, priority: int, target: Callable, args: tuple = None, kwargs: dict = None):
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
        :param count: Runs first {count} functions, ordered by priority, then by FIFO
        :param priority: If true, runs all functions with the same and highest priority. Overrides count
        :return: None
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

    def run_all(self):
        """
        Runs all targets in queue, sorted by priority
        :return: None
        """
        self._queue.sort()
        for __, target, args, kwargs in self._queue:
            target(*args, **kwargs)
        self._queue.clear()

    def clear(self):
        """
        Clears queue
        :return: None
        """
        self._queue.clear()


if __name__ == '__main__':
    import time, psutil, os
    process = psutil.Process(os.getpid())
    print(f"Memory: {process.memory_info().rss / (1024 * 1024)} MB\n")

    t1 = time.perf_counter()

    queue = PriorityQueue()
    queue.insert(2, print, ("Low priority",), {'end': ' kwargs\n'}),
    queue.insert(1, print, ("Medium Priority",))
    queue.run()  # till now, medium priority has highest priority, executes firsts
    queue.insert(0, print, ("High priority",))
    print(queue)
    queue.run(3)  # now high and low priority are present in queue, higher one executes first

    t2 = time.perf_counter()

    queue.insert(2, print, ("Low priority",))
    queue.insert(1, print, ("\nMedium Priority 2",))
    queue.insert(2, print, ("Low priority 2",))
    queue.insert(1, print, ("Medium Priority",))
    queue.run(priority=True)
    queue.run(priority=True)
    queue.run(priority=True)

    t3 = time.perf_counter()

    queue.insert(1, print, ("Medium Priority",))
    queue.insert(0, print, ("\nHigh priority",))
    queue.run_all()

    t4 = time.perf_counter()

    print(f"""\nCount run: {(t2 - t1) * 1000000} ns
Priority run: {(t3 - t2) * 1000000} ns
All run: {(t4 - t3) * 1000000} ns
Total: {(t4 - t1) * 1000000} ns""")
    print(f"Memory: {process.memory_info().rss / (1024 * 1024)} MB")
