import functools

def decorator_with_arguments(number):
    print(number)
    def my_decorator(func):
        @functools.wraps(func)
        def function_that_runs_func(*args, **kwargs):
            print('in the decorator')
            if number == 56:
                print('Not runnign the function')
            else:
                func(*args, **kwargs)
            print("After the decorator")
        return function_that_runs_func
    return my_decorator

@decorator_with_arguments(56)
def myfunction_too(x, y):
    print(x + y)

myfunction_too(57, 67)