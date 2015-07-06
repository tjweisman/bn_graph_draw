import pexpect, importlib, inspect, imp, sys, re
import sage_wrapper_internal
try:
    from decorator import decorator
except ImportError as e:
    print ("cannot find decorator module. If you are running this program "
           "from inside sage, this is expected. Otherwise, you need to install "
           "the module.")

ansi_escape = re.compile(r'\x1b[^m]*m')

class SageCommunicate:
    """class to control a running sage session and send commands to it"""
    def __init__(self):
        self.sage_ok = True
        try:
            import sage.all
        except ImportError as e:
            self.sage_ok = False
        self.sage_process = None
        self.sage_prompt = "sage:"
        self.sage_bin = "sage"
        self.is_setup = False
        self.to_load = []

    def setup(self, sage_bin, sage_prompt="sage:"):
        """initialize the path to the sage binary and the default prompt"""
        self.sage_bin = sage_bin
        self.sage_prompt = sage_prompt
        self.is_setup = True
        
    def start(self, sage_bin=None, sage_prompt="sage:"):
        """start the sage session"""
        if self.is_setup:
            if not sage_bin:
                sage_bin=self.sage_bin
            if not sage_prompt:
                sage_prompt=self.sage_prompt
        elif sage_bin:
            self.is_setup = True
        #TODO: wrap this in a try/catch
        self.sage_process = pexpect.spawn(sage_bin)
        #expect the default prompt
        self.sage_process.expect(sage_prompt)
        #special internal wrapper module imported inside sage
        self.send_command('import graph_ui.sage_wrapper_internal as sage_wrapper')
        
        #import modules we tried to import previously
        for module in self.to_load:
            self._import_module(module)

    def send_command(self, command):
        """send a command to the sage session and return the last line before
        the prompt

        """
        if self.sage_process:
            self.sage_process.sendline(command)
            self.sage_process.expect(self.sage_prompt)
            oput = ansi_escape.sub('', self.sage_process.before)
            return oput.strip().splitlines()[-1]
        return ""

    def import_module(self, module_name):
        """load a module inside the sage session"""
        if self.sage_process:
            self._import_module(module_name)
        else:
            #if we haven't started yet, add the module to a list
            self.to_load.append(module_name)
            
    def _import_module(self, module_name):
        self.send_command('import %s'%module_name)
        self.send_command('sage_wrapper.attach_sage("%s")'%module_name)

sage_comm = SageCommunicate()

#global functions to setup/start the session
def setup(sage_bin, sage_prompt="sage:"):
    sage_comm.setup(sage_bin, sage_prompt)

def start(sage_bin, sage_prompt="sage:"):
    sage_comm.start(sage_bin, sage_prompt)

def sage_started():
    return sage_comm.sage_ok or sage_comm.sage_process

def sage_wrapper(func, module_name, sage_comm):
    """decorator for functions to call from inside sage.

    takes a function func as input, and returns a function with the
    same argspec as func, which will call func inside a running sage
    session.

    """
    def _sage_wrapper(func, *args, **kwargs):
        if sage_comm.is_setup:
            arg_str = str(args)[1:-1]
            kwarg_strs = ["%s=%s"%(str(k), str(v))
                          for k,v in kwargs.iteritems()]
            arg_str = ",".join([arg_str] + kwarg_strs)
            calling_code = "%s.%s(%s)"%(module_name, func.__name__, arg_str)
            if not sage_comm.sage_process:
                sage_comm.start()
            return eval(sage_comm.send_command(calling_code))
        return None
    return decorator(_sage_wrapper, func)

def sagely_import(module_name,
                  sage_bin="sage", 
                  sage_prompt="sage:"):
    """import a module that uses sage

    if the current module is already running inside sage, then just
    import the module (more or less) normally. Otherwise, return a
    module that wraps each function in this module in a function that
    calls the other inside a sage session.

    """
    global sage_comm
    if sage_comm.sage_ok:
        #if we're inside sage, need to attach sage.all to the module
        #we import
        module = importlib.import_module(module_name)
        sage_wrapper_internal.attach_sage(module_name)
        return module
    elif module_name in sys.modules:
        #module has already been imported, don't bother starting
        #another sage process
        return sys.modules[module_name]
    else:
        sage_comm.import_module(module_name)
        module = importlib.import_module(module_name)
        members = [m[1] for m in inspect.getmembers(module)]
        functions = filter(lambda m: inspect.isfunction(m), members)
        #wrap each func and replace it in the module dict with the
        #wrapped version
        for func in functions:
            f = sage_wrapper(func, module_name, sage_comm)
            module.__dict__[func.__name__] = f
        return module
