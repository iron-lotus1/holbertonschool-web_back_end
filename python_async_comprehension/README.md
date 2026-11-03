# Python - Async Generators

## Introduction

This directory introduces **asynchronous generators**, **async comprehensions**, and **concurrent execution** in Python.

These concepts allow Python programs to perform tasks without blocking the entire program while waiting for something to finish.

For example, imagine a program that needs to:
- Wait for information from an API.
- Read data from a database.
- Download multiple files.
- Collect information from several sources.

Instead of waiting for each task to finish one at a time, asynchronous programming allows Python to manage multiple tasks efficiently.

In this directory, we will build three connected programs:

| File | Purpose |
|---|---|
| `0-async_generator.py` | Creates an asynchronous generator that produces random numbers. |
| `1-async_comprehension.py` | Collects numbers from the asynchronous generator into a list. |
| `2-measure_runtime.py` | Measures how long four asynchronous comprehensions take when executed concurrently. |

---

# 1. Understanding Asynchronous Programming

Before looking at the code, it is important to understand the difference between normal and asynchronous programming.

### Synchronous programming

Synchronous code executes instructions one after another.

For example:

```python
import time

def task_one():
    time.sleep(2)
    print("Task one finished")

def task_two():
    time.sleep(2)
    print("Task two finished")

task_one()
task_two()
```

What happens?

1. Python starts `task_one()`.
2. Python waits two seconds.
3. Task one finishes.
4. Python starts `task_two()`.
5. Python waits another two seconds.
6. Task two finishes.

**Total execution time: approximately 4 seconds.**

Python cannot move on to the second task until the first task has finished.

### Asynchronous programming

Asynchronous programming allows Python to pause a task while it is waiting and work on another task in the meantime.

This is particularly useful when dealing with operations that spend time waiting, such as network requests or timers.

Python provides the `asyncio` module to help manage asynchronous operations.

For example:

```python
import asyncio

async def task_one():
    await asyncio.sleep(2)
    print("Task one finished")

async def task_two():
    await asyncio.sleep(2)
    print("Task two finished")

async def main():
    await asyncio.gather(task_one(), task_two())

asyncio.run(main())
```

Both tasks can wait at the same time.

**Total execution time: approximately 2 seconds.**

The important keywords are:

- `async`: Declares a coroutine or asynchronous function.
- `await`: Pauses the current coroutine until an asynchronous operation completes.
- `asyncio`: Python's library for managing asynchronous tasks.

---

# 2. File: `0-async_generator.py`

## What is an asynchronous generator?

An asynchronous generator is similar to a normal Python generator, but it works with asynchronous operations.

A normal generator uses `yield` to produce values one at a time.

An asynchronous generator also uses `yield`, but it can pause and wait for asynchronous operations using `await`.

This makes it useful when generating or retrieving information takes time.

### The code

```python
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    The coroutine will loop 10 times, each time asynchronously wait 1 second,
    then yield a random number between 0 and 10. Use the random module.
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
```

## Breaking down the code

### Imports

```python
import asyncio
```

Imports Python's asynchronous programming library.

We use this module to create delays without blocking the entire program.

```python
import random
```

Imports Python's random number generator.

We use it to generate random floating-point numbers.

```python
from typing import Generator
```

Imports a type hint used to describe the values produced by the generator.

### Creating the asynchronous generator

```python
async def async_generator() -> Generator[float, None, None]:
```

Let's break this down:

- `async`: Declares an asynchronous function.
- `def`: Defines a function.
- `async_generator`: The function's name.
- `()`: The function does not require any arguments.
- `-> Generator[float, None, None]`: Describes the generator's expected type.

The three values inside `Generator` represent:

| Type | Meaning |
|---|---|
| `float` | The type of values produced by the generator. |
| `None` | The type of values that can be sent into the generator. |
| `None` | The type of the value returned when the generator finishes. |

### The for loop

```python
for _ in range(10):
```

This loop runs ten times.

`range(10)` produces ten iterations, starting at 0 and ending at 9.

The underscore `_` means we do not need to use the loop variable.

For example, instead of:

```python
for number in range(10):
    print(number)
```

We use `_` because the iteration number is not important.

### Asynchronous sleep

```python
await asyncio.sleep(1)
```

This is one of the most important lines.

It tells Python to wait for one second asynchronously.

Unlike `time.sleep(1)`, `asyncio.sleep(1)` does not block the entire event loop.

The `await` keyword allows Python to pause this coroutine while other asynchronous tasks can run.

### Generating a random number

```python
yield random.uniform(0, 10)
```

`random.uniform(0, 10)` generates a random floating-point number between 0 and 10.

For example:

```text
3.482
8.126
0.735
5.921
```

The `yield` keyword sends the generated number to whoever is consuming the generator.

Unlike `return`, which finishes a function, `yield` pauses the generator and allows it to continue later.

### How the generator works

The generator follows this sequence:

1. Start the loop.
2. Wait asynchronously for one second.
3. Generate a random number.
4. Yield the number.
5. Continue to the next iteration.
6. Repeat until ten numbers have been generated.
7. Finish the generator.

Because there are ten iterations with a one-second delay, consuming the entire generator takes approximately 10 seconds when run on its own.

### Example usage

```python
import asyncio

async_generator = __import__('0-async_generator').async_generator

async def main():
    async for number in async_generator():
        print(number)

asyncio.run(main())
```

Here we introduce another important keyword:

```python
async for
```

An asynchronous generator cannot be consumed using an ordinary `for` loop.

Instead, we use `async for` to retrieve its values asynchronously.

---

# 3. File: `1-async_comprehension.py`

## What is an async comprehension?

A comprehension is a shorter way of creating a collection, such as a list.

For example, a normal list comprehension:

```python
numbers = [number for number in range(5)]

print(numbers)
```

Output:

```text
[0, 1, 2, 3, 4]
```

An **async comprehension** works similarly, except it retrieves values from an asynchronous iterable.

This allows us to collect values from our asynchronous generator without manually writing an `async for` loop.

### The code

```python
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Collect 10 random numbers using an async comprehension over
    async_generator and return the resulting list of numbers.
    """
    return [i async for i in async_generator()]
```

## Breaking down the code

### Importing List

```python
from typing import List
```

Imports `List` from Python's typing module.

We use it to describe the type of data returned by our function.

### Importing the asynchronous generator

```python
async_generator = __import__('0-async_generator').async_generator
```

This line imports the `async_generator` function from the previous file.

Why use `__import__()`?

Python module names normally need to follow standard identifier naming rules. Since our filename begins with `0-`, we cannot import it using a regular import statement like:

```python
import 0-async_generator
```

Instead, `__import__()` allows us to load the module dynamically.

The final `.async_generator` accesses the function inside that module.

### Creating the coroutine

```python
async def async_comprehension() -> List[float]:
```

This defines an asynchronous function called `async_comprehension`.

The return type:

```python
List[float]
```

Means the function returns a list containing floating-point numbers.

### The async comprehension

```python
return [i async for i in async_generator()]
```

This is the main part of the assignment.

Let's break it down:

- `return`: Sends the finished list back to whoever called the function.
- `[ ]`: Creates a list.
- `i`: Represents each number received from the generator.
- `async for`: Retrieves values asynchronously.
- `async_generator()`: Calls the asynchronous generator from the previous file.

This single line replaces a longer approach using an empty list and a loop.

For example, the equivalent code would be:

```python
async def async_comprehension():
    numbers = []

    async for number in async_generator():
        numbers.append(number)

    return numbers
```

Both approaches collect the ten generated numbers into a list.

### Example usage

```python
import asyncio

async_comprehension = __import__(
    '1-async_comprehension'
).async_comprehension

async def main():
    numbers = await async_comprehension()

    print(numbers)
    print(len(numbers))

asyncio.run(main())
```

Possible output:

```text
[3.482, 8.126, 0.735, 5.921, 2.164,
 9.321, 4.673, 1.256, 7.845, 6.432]

10
```

Your numbers will be different because they are randomly generated.

Notice this line:

```python
numbers = await async_comprehension()
```

We use `await` because `async_comprehension()` is a coroutine.

Python must wait for the coroutine to finish collecting its numbers before assigning the result to `numbers`.

---

# 4. File: `2-measure_runtime.py`

## What is concurrency?

Concurrency means managing multiple tasks during overlapping periods of time.

Instead of waiting for one asynchronous task to finish before starting another, Python can schedule several tasks and allow them to make progress while others are waiting.

This is particularly useful for I/O-bound operations.

For example:

Imagine downloading four files.

A sequential approach might look like this:

```text
Download file 1: 10 seconds
Download file 2: 10 seconds
Download file 3: 10 seconds
Download file 4: 10 seconds

Total: 40 seconds
```

With asynchronous concurrency:

```text
Download file 1: 10 seconds
Download file 2: 10 seconds
Download file 3: 10 seconds
Download file 4: 10 seconds

Total: approximately 10 seconds
```

The tasks overlap instead of waiting for one another.

### The code

```python
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Execute async_comprehension four times concurrently using asyncio.gather,
    measure the total elapsed time, and return it.
    """
    start_time = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end_time = time.perf_counter()
    return end_time - start_time
```

## Breaking down the code

### Imports

```python
import asyncio
```

Imports the asynchronous programming library.

We need it because we will use `asyncio.gather()` to execute multiple coroutines concurrently.

```python
import time
```

Imports Python's time module.

We use it to measure how long our program takes to execute.

### Importing async_comprehension

```python
async_comprehension = __import__('1-async_comprehension').async_comprehension
```

Imports the asynchronous comprehension function from the previous file.

This function collects ten random numbers, taking approximately ten seconds per execution.

### Creating the coroutine

```python
async def measure_runtime() -> float:
```

Defines an asynchronous function called `measure_runtime`.

It returns a floating-point number representing the total execution time.

### Starting the timer

```python
start_time = time.perf_counter()
```

`time.perf_counter()` provides a high-resolution timer.

It is particularly useful for measuring how long an operation takes.

We store the starting time in `start_time`.

### Running tasks concurrently

```python
await asyncio.gather(*(async_comprehension() for _ in range(4)))
```

This is the most important line in this file.

Let's break it down.

**1. The generator expression**

```python
(async_comprehension() for _ in range(4))
```

Creates four coroutine objects by calling `async_comprehension()` four times.

It does not execute them one after another.

**2. The unpacking operator**

```python
*
```

The asterisk unpacks the generated coroutine objects into separate arguments.

This is necessary because `asyncio.gather()` accepts multiple awaitables as arguments.

Conceptually, the expression becomes:

```python
asyncio.gather(
    async_comprehension(),
    async_comprehension(),
    async_comprehension(),
    async_comprehension()
)
```

**3. asyncio.gather()**

```python
asyncio.gather(...)
```

Schedules the supplied coroutines so they can run concurrently.

Each coroutine generates ten random numbers, waiting one second between each number.

Because all four coroutines are waiting asynchronously, their execution overlaps.

**4. await**

```python
await asyncio.gather(...)
```

Waits until all four coroutines have finished.

The results are returned by `gather()`, although this assignment does not need to store them.

### Stopping the timer

```python
end_time = time.perf_counter()
```

Once all four tasks have completed, we record the ending time.

### Calculating the runtime

```python
return end_time - start_time
```

Subtracts the starting time from the ending time.

This gives us the total elapsed time.

Since each asynchronous comprehension takes approximately ten seconds, the expected runtime is approximately:

```text
10 seconds
```

Not 40 seconds!

This demonstrates the benefit of concurrency.

### Example usage

```python
import asyncio

measure_runtime = __import__(
    '2-measure_runtime'
).measure_runtime

async def main():
    runtime = await measure_runtime()

    print(runtime)

asyncio.run(main())
```

Possible output:

```text
10.01
```

The exact time will vary depending on your computer and system load.

---

# 5. How All Three Files Work Together

The three files build on one another.

Each file has a specific responsibility.

### Program flow

```text
              START
                |
                v
       0-async_generator.py
                |
                v
       Generate random numbers
       Wait 1 second per number
       Yield 10 numbers
                |
                v
     1-async_comprehension.py
                |
                v
       Collect generated numbers
          into a Python list
                |
                v
       2-measure_runtime.py
                |
                v
       Create 4 coroutines
                |
                v
        asyncio.gather()
                |
                v
       Run all 4 concurrently
                |
                v
       Wait for all tasks to finish
                |
                v
       Calculate elapsed time
                |
                v
                END
```

### Understanding the execution time

| Execution method | Expected runtime |
|---|---:|
| One async comprehension | ~10 seconds |
| Four sequential comprehensions | ~40 seconds |
| Four concurrent comprehensions | ~10 seconds |

The important thing to understand is that concurrency does not make each individual generator produce numbers faster.

Each generator still waits one second between numbers.

Instead, concurrency allows all four generators to make progress during the same time period.

---

# 6. Important Python Concepts to Remember

Here is a summary of the main concepts introduced in this directory.

| Concept | Explanation |
|---|---|
| `async` | Defines an asynchronous function. |
| `await` | Waits for an asynchronous operation without blocking the event loop. |
| `yield` | Produces a value from a generator while preserving its state. |
| `async for` | Iterates over an asynchronous iterable. |
| Async generator | Produces values asynchronously, one at a time. |
| Coroutine | An asynchronous function that can be paused and resumed. |
| List comprehension | A concise way to create a list. |
| Async comprehension | A concise way to collect values from an asynchronous iterable. |
| `asyncio.sleep()` | Pauses a coroutine asynchronously. |
| `asyncio.gather()` | Runs multiple awaitables concurrently and collects their results. |
| `time.perf_counter()` | Measures elapsed execution time accurately. |

### One important distinction

These three keywords are related but do different things:

```python
async
await
yield
```

- `async` defines asynchronous behaviour.
- `await` pauses a coroutine while waiting for an operation.
- `yield` produces a value from a generator.

Understanding the difference is essential when working with asynchronous Python.

---

# 7. Practice Exercises

Try these exercises to check whether you understand the code.

### Exercise 1: Change the number of iterations

In `0-async_generator.py`, find:

```python
for _ in range(10):
```

Change it to:

```python
for _ in range(5):
```

**Questions:**
1. How many random numbers will the generator produce?
2. How long will one complete generator execution take?
3. What will happen to the length of the list returned by `async_comprehension()`?

### Exercise 2: Change the random number range

Find:

```python
yield random.uniform(0, 10)
```

Change it to:

```python
yield random.uniform(1, 100)
```

**Questions:**
1. What is the new minimum value?
2. What is the new maximum value?
3. Will the execution time change?

### Exercise 3: Increase concurrency

In `2-measure_runtime.py`, find:

```python
await asyncio.gather(*(async_comprehension() for _ in range(4)))
```

Change it to:

```python
await asyncio.gather(*(async_comprehension() for _ in range(8)))
```

**Questions:**
1. How many coroutines are now running?
2. Will the execution time double?
3. Why or why not?

### Exercise 4: Understand async for

Rewrite the list comprehension in `1-async_comprehension.py` using a normal-looking asynchronous loop.

Replace:

```python
return [i async for i in async_generator()]
```

With your own implementation using:
- An empty list.
- An `async for` loop.
- `.append()` to add each number.
- `return` to return the completed list.

---

# 8. Final Takeaways

By completing these exercises, you should understand how Python handles asynchronous generators and concurrent tasks.

The most important lessons are:

1. **Asynchronous generators** allow you to produce values while performing asynchronous operations.
2. **Async comprehensions** provide a concise way to collect values from asynchronous generators.
3. **Coroutines** allow asynchronous functions to pause and resume.
4. **`asyncio.gather()`** allows multiple coroutines to execute concurrently.
5. **`time.perf_counter()`** allows you to measure how long your asynchronous operations take.

The biggest takeaway from this project is understanding that asynchronous programming is particularly useful when your program spends time waiting.

Instead of making your program wait for each operation individually, you can allow multiple operations to make progress concurrently.

This is a fundamental concept used in modern Python applications, especially when working with APIs, networking, databases, and other I/O-bound operations.
