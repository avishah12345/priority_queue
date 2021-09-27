# priority_queue
Run functions based on their priority. Higher priority functions are run first, followed by lower priority ones.

## Why would one want to use a _priority queue_?
This concept saved one of NASA's moon missions. The computer focused on the 
problem first, then the other basic tasks. Although functionally not required, 
it is useful in cases where errors and abrupt stops are common.

## Usage
### Init
`queue = PriorityQueue()`

An optional queue parameter can be passed to initialize the queue.
```python
queue = PriorityQueue([
    (priority, target, args, kwargs),
    (priority2, target2, args2, kwargs2)
])
```

### Insert
To insert a function into the queue:

`queue.insert(priority, target, args, kwargs)`

### Insert many
To insert many functions into the queue:

```python
queue.insert_many([
    (priority, target, args, kwargs),
    (priority2, target2, args2, kwargs2)
])
```

### Run
To run first n functions:

`queue.run(n)  # n defaults to 1`

To run all functions with the same and highest priority:

`queue.run(priority=True)`

### Run all
`queue.run_all()`

### Remove
To remove, you need to store the return value when inserting

```python
remove_me = queue.insert(priority, target, args, kwargs)
# some code
queue.remove(remove_me)
```

You can remove items even if they have been queued via insert_many:

```python
functions = [
    (priority, target, args, kwargs),
    (priority2, target2, args2, kwargs2)
]
queue.insert_many(functions)
# some code
queue.remove(functions[0])
```

### Remove many
To remove a bunch of functions at once:

```python
functions = [
    (priority, target, args, kwargs),
    (priority2, target2, args2, kwargs2)
]
queue.insert_many(functions)
# some code
queue.remove(functions)
```

### Clear queue
To clear the queue:

`queue.clear()`

### Length
To get the length of the queue:

`print(len(queue))`
