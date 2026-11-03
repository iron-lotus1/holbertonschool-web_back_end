# Python - Async and Await

## Introduction

This project introduces **Asynchronous Programming in Python** using the `asyncio` module.

When writing Python programs, code normally executes one instruction after another. This is called **synchronous programming**.

However, sometimes a program needs to wait for something to happen. For example:

- Waiting for a website to respond.
- Downloading information from the internet.
- Reading data from another server.
- Waiting for a timer.
- Handling multiple tasks that involve waiting.

If we use normal synchronous code, Python may sit and wait for one operation to finish before moving on to the next.

Asynchronous programming allows Python to work on other tasks while waiting for an operation to finish.

This can make programs much more efficient, particularly when dealing with operations that involve waiting.

---

# 1. Understanding Asynchronous Programming

Before looking at the code, let's understand some important concepts.

### Synchronous programming

Synchronous programming executes instructions one at a time.

For example:

```python
import time

def task_one():
    time.sleep(3)
    print("Task one finished")

def task_two():
    print("Task two finished")

task_one()
task_two()
```

### What happens?

1. Python starts `task_one()`.
2. Python waits for 3 seconds.
3. Python prints `Task one finished`.
4. Python starts `task_two()`.
5. Python prints `Task two finished`.

The second task cannot start until the first task finishes.

### Asynchronous programming

Asynchronous programming allows Python to switch between tasks while waiting.

Instead of using `time.sleep()`, we use `asyncio.sleep()`.

```python
import asyncio

async def task_one():
    await asyncio.sleep(3)
    print("Task one finished")

async def task_two():
    print("Task two finished")

async def main():
    await asyncio.gather(task_one(), task_two())

asyncio.run(main())
```

Here, Python can execute `task_two()` while `task_one()` is waiting.

**Important:** Asynchronous programming does not necessarily mean that Python is using multiple CPU cores. Instead, it allows tasks to make progress without blocking the entire program while they wait.

---

# 2. Important Python Concepts

Before moving through the project, let's understand the keywords and functions used throughout the files.

| Keyword / Function | Explanation |
|---|---|
| `async` | Declares an asynchronous function, also called a coroutine function. |
| `await` | Waits for an asynchronous operation to finish while allowing other tasks to run. |
| `asyncio` | Python's library for asynchronous programming. |
| `asyncio.sleep()` | Waits for a specified amount of time without blocking the event loop. |
| `asyncio.run()` | Starts an event loop and executes a coroutine. |
| `asyncio.create_task()` | Schedules a coroutine to run as an asyncio task. |
| `asyncio.as_completed()` | Provides tasks in the order they finish. |
| `random.uniform()` | Generates a random floating-point number within a range. |
| `time.time()` | Returns the current time, useful for measuring elapsed time. |
| `List[float]` | A type hint indicating a list of floating-point numbers. |

### What is a coroutine?

A coroutine is a special type of function that can pause its execution and resume later.

You create one by using `async def`.

```python
async def say_hello():
    print("Hello!")
```

Calling this function does not immediately execute its body in the same way as a normal function.

Instead, it returns a coroutine object that needs to be awaited or scheduled.

For example:

```python
import asyncio

async def say_hello():
    print("Hello!")

asyncio.run(say_hello())
```

### What is an event loop?

The event loop is responsible for managing asynchronous tasks.

Think of it as a manager that:

1. Starts asynchronous tasks.
2. Tracks which tasks are running.
3. Notices when a task needs to wait.
4. Allows other tasks to run.
5. Resumes tasks when their waiting operation completes.

---

# 3. File 0 - Basic Async Syntax

**File:** `0-basic_async_syntax.py`

### Purpose

This file introduces the basic syntax of asynchronous programming.

It contains one coroutine called `wait_random()`.

The function generates a random delay, waits for that amount of time, and returns the delay.

### The code

```python
import asyncio
import random

async def wait_random(max_delay: int = 10) -> float:
    """
    Waits for a random delay between 0 and max_delay seconds
    and returns it.
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
```

### Understanding the code

**1. Importing asyncio**

```python
import asyncio
```

Imports Python's asynchronous programming library.

We need this because we want to use `asyncio.sleep()`.

**2. Importing random**

```python
import random
```

Imports Python's random number generator.

We use it to generate a random delay.

**3. Creating the coroutine**

```python
async def wait_random(max_delay: int = 10) -> float:
```

Let's break this down:

- `async def` tells Python this is an asynchronous function.
- `wait_random` is the function name.
- `max_delay` is an argument.
- `= 10` means the default maximum delay is 10 seconds.
- `-> float` indicates that the function returns a floating-point number.

**4. Generating a random delay**

```python
delay = random.uniform(0, max_delay)
```

`random.uniform()` generates a random floating-point number between two values.

For example, if:

```python
max_delay = 5
```

Possible results include:

```text
0.52
1.84
3.27
4.91
```

Each execution can generate a different number.

**5. Waiting asynchronously**

```python
await asyncio.sleep(delay)
```

This is one of the most important lines.

It tells Python to wait for the number of seconds stored in `delay`.

The `await` keyword allows the event loop to work on other tasks while this coroutine is waiting.

**6. Returning the result**

```python
return delay
```

Once the waiting period finishes, the function returns the random delay.

### Example usage

```python
import asyncio

async def main():
    result = await wait_random(5)
    print(result)

asyncio.run(main())
```

Possible output:

```text
3.48291
```

Your actual output will vary because the delay is random.

### What you have learned

- How to create a coroutine.
- How to use `async`.
- How to use `await`.
- How to generate random numbers.
- How to wait without blocking the event loop.

---

# 4. File 1 - Concurrent Coroutines

**File:** `1-concurrent_coroutines.py`

### Purpose

This file builds on the previous exercise.

Instead of running one `wait_random()` coroutine, we now run multiple coroutines concurrently.

We create a function called `wait_n()`.

It starts `wait_random()` multiple times and collects the results in the order they finish.

### The code

```python
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random

async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawns wait_random n times with max_delay and returns delays
    in ascending order of completion without using sort().
    """
    delays: List[float] = []

    tasks = [
        asyncio.create_task(wait_random(max_delay))
        for _ in range(n)
    ]

    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)

    return delays
```

### Understanding the code

**1. Importing asyncio**

```python
import asyncio
```

We need asyncio to create and manage multiple asynchronous tasks.

**2. Importing List**

```python
from typing import List
```

This allows us to describe the expected type of the returned list.

**3. Importing wait_random**

```python
wait_random = __import__('0-basic_async_syntax').wait_random
```

Normally, Python imports modules using:

```python
import module_name
```

However, Python module names cannot normally start with a number using standard import syntax.

The `__import__()` function allows us to import this module dynamically.

We then access its `wait_random` function.

**4. Creating the asynchronous function**

```python
async def wait_n(n: int, max_delay: int) -> List[float]:
```

This function accepts two arguments:

- `n`: The number of coroutines to execute.
- `max_delay`: The maximum random delay for each coroutine.

It returns a list of floating-point numbers.

**5. Creating an empty list**

```python
delays: List[float] = []
```

This list stores the results returned by each coroutine.

Initially, it is empty.

**6. Creating multiple tasks**

```python
tasks = [
    asyncio.create_task(wait_random(max_delay))
    for _ in range(n)
]
```

This is a list comprehension.

It creates `n` asyncio tasks.

For example:

```python
n = 5
max_delay = 5
```

Python creates five separate tasks.

Each task runs `wait_random(5)` and generates its own random delay.

`asyncio.create_task()` schedules the coroutine to run on the event loop.

**7. Processing tasks as they finish**

```python
for task in asyncio.as_completed(tasks):
```

This is another important part of the project.

`asyncio.as_completed()` allows us to process tasks in the order they finish.

For example, imagine five tasks have these delays:

| Task | Delay |
|---|---:|
| Task 1 | 4 seconds |
| Task 2 | 1 second |
| Task 3 | 3 seconds |
| Task 4 | 2 seconds |
| Task 5 | 5 seconds |

The completion order will be:

```text
Task 2
Task 4
Task 3
Task 1
Task 5
```

Notice that this is not the same as the order in which the tasks were created.

**8. Awaiting each task**

```python
delay = await task
```

This retrieves the result of the completed task.

**9. Adding the result to the list**

```python
delays.append(delay)
```

The result is added to the list.

Because we are processing tasks as they finish, the list stores their completion order.

**10. Returning the list**

```python
return delays
```

Once all tasks have completed, we return the list.

### Example usage

```python
import asyncio

async def main():
    results = await wait_n(5, 5)
    print(results)

asyncio.run(main())
```

Possible output:

```text
[0.52, 1.13, 2.48, 3.71, 4.92]
```

The values will be different each time.

### What you have learned

- How to create multiple asynchronous tasks.
- How to use `asyncio.create_task()`.
- How to use list comprehensions.
- How to use `asyncio.as_completed()`.
- How to collect results in completion order.

---

# 5. File 2 - Measure Runtime

**File:** `2-measure_runtime.py`

### Purpose

Now that we understand how to execute multiple coroutines concurrently, we want to measure how long they take to finish.

This file contains a normal Python function called `measure_time()`.

It measures the total execution time of `wait_n()` and calculates the average time per coroutine.

### The code

```python
import time
import asyncio

wait_n = __import__('1-concurrent_coroutines').wait_n

def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time for wait_n(n, max_delay)
    and returns the average time per execution (total_time / n).
    """
    start_time = time.time()

    asyncio.run(wait_n(n, max_delay))

    end_time = time.time()

    return (end_time - start_time) / n
```

### Understanding the code

**1. Importing time**

```python
import time
```

The `time` module provides functions for working with time.

We use it to calculate how long our program takes to execute.

**2. Importing asyncio**

```python
import asyncio
```

We need asyncio because we are executing an asynchronous coroutine.

**3. Importing wait_n**

```python
wait_n = __import__('1-concurrent_coroutines').wait_n
```

We import the function created in the previous file.

**4. Creating the function**

```python
def measure_time(n: int, max_delay: int) -> float:
```

Unlike the previous functions, this is a normal synchronous function.

It accepts:

- `n`: Number of coroutines.
- `max_delay`: Maximum random delay.

It returns a floating-point number representing the average execution time.

**5. Recording the starting time**

```python
start_time = time.time()
```

This records the current time before executing the coroutines.

**6. Running the asynchronous function**

```python
asyncio.run(wait_n(n, max_delay))
```

`asyncio.run()` starts an event loop and executes `wait_n()`.

It waits until all the coroutines finish.

**7. Recording the finishing time**

```python
end_time = time.time()
```

Once all tasks have finished, we record the current time again.

**8. Calculating the average**

```python
return (end_time - start_time) / n
```

We subtract the starting time from the ending time to calculate the total execution time.

Then we divide that result by `n`.

### Example calculation

Imagine we execute:

```python
measure_time(5, 5)
```

Suppose the total execution time is approximately 4 seconds.

The calculation is:

```text
Total execution time = 4 seconds
Number of coroutines = 5

Average time = 4 / 5

Average time = 0.8 seconds
```

The function returns approximately:

```text
0.8
```

**Important:** This is the average share of the total elapsed time per coroutine. It is not the actual execution duration of each individual coroutine.

### Why is this useful?

This exercise demonstrates an important advantage of asynchronous programming.

If five tasks each wait for a random period, running them sequentially could take the sum of all their waiting times.

Running them concurrently means the total waiting time is generally closer to the longest individual delay.

---

# 6. File 3 - Tasks

**File:** `3-tasks.py`

### Purpose

This file introduces another way to work with coroutines.

Previously, we created tasks directly inside `wait_n()`.

Now we create a separate function called `task_wait_random()`.

Its job is to take a coroutine and turn it into an asyncio task.

### The code

```python
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random

def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Takes an integer max_delay and returns an asyncio
    Task wrapping wait_random.
    """
    return asyncio.create_task(wait_random(max_delay))
```

### Understanding the code

**1. Importing asyncio**

```python
import asyncio
```

We need this to create an asyncio task.

**2. Importing wait_random**

```python
wait_random = __import__('0-basic_async_syntax').wait_random
```

We import the coroutine from the first file.

**3. Creating the function**

```python
def task_wait_random(max_delay: int) -> asyncio.Task:
```

This is a normal Python function.

It accepts one argument:

- `max_delay`: The maximum number of seconds to wait.

It returns an `asyncio.Task`.

Notice that this function does not use `async def`.

That is because it does not need to be a coroutine itself. It simply creates and returns a task.

**4. Creating the task**

```python
return asyncio.create_task(wait_random(max_delay))
```

This line does two things:

1. Calls `wait_random(max_delay)` to create a coroutine object.
2. Passes that coroutine to `asyncio.create_task()` to schedule it.

The resulting task is returned.

### Example usage

```python
import asyncio

async def main():
    task = task_wait_random(5)

    result = await task

    print(result)

asyncio.run(main())
```

Possible output:

```text
2.73
```

### Understanding the difference

There is an important difference between a coroutine and a task.

**Coroutine:**

```python
coroutine = wait_random(5)
```

This creates a coroutine object.

It has not been scheduled as an asyncio task.

**Task:**

```python
task = asyncio.create_task(wait_random(5))
```

This schedules the coroutine to run on the event loop.

Think of it this way:

- A coroutine describes an asynchronous operation.
- A task schedules that operation to run.

### What you have learned

- How to create an asyncio task.
- How to separate task creation into its own function.
- The difference between a coroutine and a task.
- Why a normal function can return an asynchronous task.

---

# 7. File 4 - Tasks and Concurrent Execution

**File:** `4-tasks.py`

### Purpose

This file builds on the previous exercise.

Instead of calling `asyncio.create_task()` directly, we use our new `task_wait_random()` function.

We create a function called `task_wait_n()`.

It schedules multiple tasks and collects their results in the order they complete.

### The code

```python
import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random

async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Executes task_wait_random n times with specified max_delay
    and returns the list of delays in ascending order as they complete.
    """
    delays: List[float] = []

    tasks = [
        task_wait_random(max_delay)
        for _ in range(n)
    ]

    for task in asyncio.as_completed(tasks):
        delay = await task
        delays.append(delay)

    return delays
```

### Understanding the code

**1. Importing asyncio and List**

```python
import asyncio
from typing import List
```

We need asyncio to manage tasks and List to describe our return type.

**2. Importing task_wait_random**

```python
task_wait_random = __import__('3-tasks').task_wait_random
```

We import the helper function from the previous file.

**3. Creating the asynchronous function**

```python
async def task_wait_n(n: int, max_delay: int) -> List[float]:
```

This function accepts:

- `n`: Number of tasks to create.
- `max_delay`: Maximum random delay for each task.

It returns a list of floating-point numbers.

**4. Creating an empty list**

```python
delays: List[float] = []
```

This will store the results.

**5. Creating multiple tasks**

```python
tasks = [
    task_wait_random(max_delay)
    for _ in range(n)
]
```

This creates `n` tasks using the helper function from `3-tasks.py`.

For example:

```python
n = 4
max_delay = 5
```

Four separate tasks are scheduled.

Each task independently calls `wait_random(5)`.

**6. Processing tasks as they finish**

```python
for task in asyncio.as_completed(tasks):
```

This processes the tasks in their completion order.

**7. Getting each result**

```python
delay = await task
```

We wait for the completed task and retrieve its result.

**8. Saving the result**

```python
delays.append(delay)
```

We add the result to our list.

**9. Returning the results**

```python
return delays
```

Once all tasks have completed, we return the list.

### Example usage

```python
import asyncio

async def main():
    results = await task_wait_n(5, 5)
    print(results)

asyncio.run(main())
```

Possible output:

```text
[0.34, 1.26, 2.14, 3.67, 4.81]
```

Again, your results will vary.

---

# 8. How All the Files Connect

The five files build on each other.

Each exercise introduces a new concept while reusing the previous functions.

### Project structure

```text
python_async_function/
│
├── 0-basic_async_syntax.py
│
├── 1-concurrent_coroutines.py
│
├── 2-measure_runtime.py
│
├── 3-tasks.py
│
└── 4-tasks.py
```

### How the files depend on each other

```text
0-basic_async_syntax.py
        |
        | Provides wait_random()
        |
        v
1-concurrent_coroutines.py
        |
        | Uses wait_random()
        | Creates multiple concurrent tasks
        |
        v
2-measure_runtime.py
        |
        | Uses wait_n()
        | Measures execution time
        |
        |
0-basic_async_syntax.py
        |
        | Provides wait_random()
        |
        v
3-tasks.py
        |
        | Uses wait_random()
        | Returns an asyncio.Task
        |
        v
4-tasks.py
        |
        | Uses task_wait_random()
        | Creates multiple tasks
        | Collects results as they finish
```

### The overall progression

| File | Main concept | What it teaches |
|---|---|---|
| `0-basic_async_syntax.py` | Coroutines | Creating and awaiting asynchronous functions. |
| `1-concurrent_coroutines.py` | Concurrency | Running multiple coroutines together. |
| `2-measure_runtime.py` | Performance | Measuring execution time. |
| `3-tasks.py` | Tasks | Converting a coroutine into an asyncio task. |
| `4-tasks.py` | Task concurrency | Managing multiple tasks using a helper function. |

---

# 9. Important Differences to Remember

These concepts are easy to confuse when learning asynchronous programming.

### `async def` versus `def`

```python
async def my_coroutine():
    await asyncio.sleep(1)
```

Creates a coroutine function.

```python
def my_function():
    return "Hello"
```

Creates a normal synchronous function.

### `await` versus `asyncio.create_task()`

`await` waits for an asynchronous operation to complete.

```python
result = await wait_random(5)
```

`asyncio.create_task()` schedules a coroutine to run as a task.

```python
task = asyncio.create_task(wait_random(5))
```

You can then await the task:

```python
result = await task
```

### `asyncio.as_completed()` versus `asyncio.gather()`

Both can be used to manage multiple asynchronous operations.

However, they behave differently.

**`asyncio.gather()`**

```python
results = await asyncio.gather(
    wait_random(5),
    wait_random(5),
    wait_random(5)
)
```

Returns results in the same order as the coroutines were supplied.

**`asyncio.as_completed()`**

```python
tasks = [
    asyncio.create_task(wait_random(5))
    for _ in range(3)
]

results = []

for task in asyncio.as_completed(tasks):
    results.append(await task)
```

Returns results in the order the tasks finish.

This distinction is particularly important for this project.

---

# 10. Practice Exercises

Try these exercises to make sure you understand the concepts rather than simply copying the code.

### Exercise 1 - Change the default delay

Open `0-basic_async_syntax.py`.

Change the default maximum delay from 10 seconds to 5 seconds.

**Question:** What happens if you call `wait_random()` without passing an argument?

<details>
<summary>Think about the answer</summary>

The function uses the default value of 5 seconds because no argument was supplied.

</details>

### Exercise 2 - Run more tasks

Open `1-concurrent_coroutines.py`.

Call:

```python
await wait_n(10, 5)
```

**Questions:**

1. How many coroutines are created?
2. What is the maximum possible delay for each coroutine?
3. Why don't the delays necessarily appear in the order the tasks were created?

### Exercise 3 - Understand task creation

Open `3-tasks.py`.

Try creating a task using:

```python
task = task_wait_random(3)
```

Then retrieve its result using:

```python
result = await task
```

**Question:** What is the difference between the task and the result?

### Exercise 4 - Measure different workloads

Open `2-measure_runtime.py`.

Try:

```python
print(measure_time(5, 5))
print(measure_time(10, 5))
print(measure_time(20, 5))
```

**Questions:**

1. Does doubling the number of coroutines double the execution time?
2. Why does asynchronous execution help here?
3. What happens when you increase `max_delay`?

### Exercise 5 - Create your own coroutine

Create a new function called `wait_message()`.

Requirements:

1. It must be asynchronous.
2. It accepts a message and a delay.
3. It waits using `asyncio.sleep()`.
4. It prints the message after waiting.

Example:

```python
async def wait_message(message, delay):
    # Your code here
    pass
```

Try