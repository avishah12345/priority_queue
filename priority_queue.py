from typing import Callable, List, Optional, Tuple


class PriorityQueue:
    __slots__ = ('_queue', )
    def __init__(self, queue: List[Tuple[int, Callable, Optional[tuple], Optional[dict]]]=None):
        """
        :param queue: Initial queue.
        """
        self._queue = queue or list()

    def __repr__(self):
        self._queue.sort()

        def mapper(item):
            priority, target, args, kwargs = self._unpack(item)
            return f"\n\t({priority=}, {target=}, {args=}, {kwargs=})"

        t = ','.join(map(mapper, self._queue)) + '\n' if self._queue else ''
        return f"PriorityQueue(queue=[{t}])"

    def __len__(self):
        return len(self._queue)

    def _unpack(self, item):
        item_len = len(item)
        if item_len == 2:
            return *item, tuple(), dict()
        elif item_len == 3:
            if type(item[2]) is tuple:
                return *item, dict()
            else:
                return item[0:2], tuple(), item[3]
        return item

    def insert(self, priority: int, target: Callable, args: tuple = None, kwargs: dict = None):
        """
        :param priority: Lower the value, higher the priority
        :param target: Callable
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: Tuple pointer to item in queue. Can be used to remove item from queue later
        """
        item = [priority, target]
        if args: item.append(args)
        if kwargs: item.append(kwargs)
        self._queue.append(tuple(item))
        return self._queue[-1]

    def insert_many(self, queue: List[Tuple[int, Callable, Optional[tuple], Optional[dict]]]):
        """
        :param queue: Performs multiple inserts at once. List[Tuple[int, Callable, Optional[tuple], Optional[dict]]]
        :return: None
        """
        self._queue.extend(queue)

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
            for _, target, args, kwargs in map(self._unpack, items):
                target(*args, **kwargs)
            del self._queue[:len(items)]
            return
        for _ in range(count):
            try: __, target, args, kwargs = self._unpack(self._queue.pop(0))
            except IndexError: return
            else: target(*args, **kwargs)

    def run_all(self):
        """
        Runs all targets in queue, sorted by priority
        :return: None
        """
        self._queue.sort()
        for __, target, args, kwargs in map(self._unpack, self._queue):
            target(*args, **kwargs)
        self._queue.clear()

    def remove(self, item):
        """
        :param item: Tuple pointer to item in queue
        :return: None
        """
        self._queue.remove(item)

    def remove_many(self, items):
        for item in items:
            self._queue.remove(item)

    def clear(self):
        """
        Clears queue
        :return: None
        """
        self._queue.clear()


if __name__ == '__main__':
    import time

    # Create empty function for testing speed
    def nothing(*args, **kwargs):
        # print(*args, **kwargs)
        pass


    def get_time():
        global t
        return  (- t + (t := time.perf_counter())) * 1000000

    start = t = time.perf_counter()

    print(f"Normal: {get_time()} us")

    # Create instance
    queue = PriorityQueue([
        (30, nothing, ("Low priority",)),
        (10, nothing, ("High priority", "arg2"), {'end': ' kwargs\n'}),  # Lower value = high priority; runs first
        (20, nothing, ("Medium priority",))
    ])
    print(f"Init insert many: {get_time()} us")
    print(queue)
    print(f"Repr: {get_time()} us")
    queue.run(2)
    print(f"Count run: {get_time()} us")

    r = [(i, nothing, (f"Priority: {i}",)) for i in range(5, 0, -1)]
    queue.insert_many(r)
    print(f"Insert many: {get_time()} us")
    queue.remove_many(r[1:])
    print(f"Remove many: {get_time()} us")
    len(queue)
    print(f"Len: {get_time()} us")
    queue.run_all()
    print(f"Run all: {get_time()} us")

    queue.insert(20, nothing, ("Insert", ))
    r = queue.insert(20, nothing, ("Insert 2", ))
    queue.insert(20, nothing, ("Insert 3", ))
    print(f"Insert: {get_time()} ns")
    queue.remove(r)
    print(f"Remove: {get_time()} us")
    queue.run(priority=True)
    print(f"Priority run: {get_time()} us")

    print(f"Total: {(time.perf_counter() - start) * 1000000} us")
