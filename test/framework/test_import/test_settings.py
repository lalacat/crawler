from test.framework.test_import.test_loadobject import load_object
from test.framework.test_import import setting_import

def iter_default_settings():
    """Return the default settings as an iterator of (name, value) tuples"""
    for name in dir(setting_import):
        if name.isupper():
            yield name, getattr(setting_import, name)

for name,value in iter_default_settings():
    print(name,value)
