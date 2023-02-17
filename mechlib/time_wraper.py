import time

def measure_time(func):
  def wrapper(*args, **kwargs):
    start_time = time.perf_counter()  # Get the current time
    result = func(*args, **kwargs)  # Call the function
    end_time = time.perf_counter()  # Get the current time again
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Elapsed time for function '{func.__name__}': {elapsed_time:.3f} seconds")
    return result
  return wrapper

