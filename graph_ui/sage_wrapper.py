import pexpect, importlib, inspect, imp
from decorator import decorator

sage_ok = True
sage_process = None

try:
    import sage.all
except ImportError as e:
    sage_ok = False

def start_sage(sage_bin, sage_prompt):
    sage_process = pexpect.spawn(sage_bin)
    #expect the default prompt
    sage_process.expect(sage_prompt)
    return sage_process

def send_command(sage_process, command):
    sage_process.sendline(command)    

def sage_wrapper(func, sage_process, prompt="sage:"):
    def _sage_wrapper(func, *args, **kwargs):
            arg_str = str(args)[1:-1]
            kwarg_strs = ["%s=%s"%(str(k), str(v))
                          for k,v in kwargs.iteritems()]
            arg_str = ",".join([arg_str] + kwarg_strs)
            calling_code = "%s(%s)"%(func.__name__, arg_str)
            send_command(sage_process, calling_code)
            sage_process.expect(calling_code)
            sage_process.expect(prompt)
            return sage_process.before
    return decorator(_sage_wrapper, func)

def sagely_import(module_name, 
                  module_filename=None,
                  sage_bin="sage", 
                  sage_prompt="sage:"):
    global sage_ok
    global sage_process
    if sage_ok:
        return importlib.import_module(module_name)
    elif module_filename:
        if not sage_process:
            sage_process = start_sage(sage_bin, sage_prompt)
        sage_process.sendline('load("%s")'%module_filename)
        sage_process.expect(sage_prompt)
        module = importlib.import_module(module_name)
        members = [m[1] for m in inspect.getmembers(module)]
        functions = filter(lambda m: inspect.isfunction(m), members)
        wrapper_module = imp.new_module(module_name)
        for func in functions:
            f = sage_wrapper(func, sage_process, sage_prompt)
            wrapper_module.__dict__[func.__name__] = f
        return wrapper_module
    else:
        raise Exception("a module filename must be provided"
                        "if not already a child of a sage process")

