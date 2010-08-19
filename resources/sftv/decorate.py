def trace(func):
    def wrapper(*args, **kwargs):
        print 'TRACING: entering ' + func.__name__
        result = func(*args, **kwargs)
        print 'TRACING: leave ' + str(func.__class__) + '::' + func.__name__
        return result
    return wrapper
