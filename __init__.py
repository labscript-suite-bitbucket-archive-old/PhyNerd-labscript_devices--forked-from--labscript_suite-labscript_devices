import sys

__version__ = '0.1.0-dev'

def ClassRegister(object):
    """A register for looking up classes by module name.  Provides a
     decorator and a method for looking up classes decorated with it,
     importing as necessary."""
    def __init__(self, instancename):
        self.registered_classes = {}
        # The name given to the instance in this namespace, so we can use it in error messages:
        self.instancename = instancename
        
    def __call__(self, cls):
        """Adds the class to the register so that it can be looked up later
        by module name"""
        # Add an attribute to the class so it knows its own name in case
        # it needs to look up other classes in the same module:
        cls.labscript_device_name = cls_.__module__.split('.')[-1]
        # Add it to the register:
        self.registered_classes[cls.labscript_device_name] = cls
        return cls
        
    def __getitem__(self, name):
        try:
            return self.registered_classes[name]:
        except KeyError:
            pass
        # If we haven't seen that class, let's see if we can import it:
        full_module_name = __name__ + '.' + name
        if full_module_name in sys.modules:
            # Hm, already imported but not in our register. Maybe the user forgot to decorate it?
            raise ValueError('No class found in module %s, did you forget to decorate the class definition with @%s?'%(self.description))


def LabscriptDevice(cls):
    cls.labscript_device_name = cls.__module__.split('.')[-1]
    return cls

def BLACSTab(cls):
    raise NotImplementedError

def BLACSWorker(cls):
    raise NotImplementedError
    
def RunviewerParser(cls):
    raise NotImplementedError
    
def get_labscript_device(name):
    raise NotImplementedError
    
def get_BLACS_tab(name):
    raise NotImplementedError

def get_BLACS_worker(name):
    raise NotImplementedError
        
def get_runviewer_parser(name):
    raise NotImplementedError
    

