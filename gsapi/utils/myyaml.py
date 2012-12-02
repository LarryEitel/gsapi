from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# http://pyyaml.org/wiki/PyYAMLDocumentation

def pyObj(yamlFilePath):
    "Returns python object from yaml file."
    try:
    	return load(open(yamlFilePath, 'r'), Loader=Loader)
    except:
    	return None

