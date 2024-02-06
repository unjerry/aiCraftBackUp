import importlib
import sys
sys.path.append(".\cc")
print(sys.path)

# Let's say we have a variable that contains the name of the module we want to import
# spec = importlib.util.spec_from_file_location("module.name", "cc\parameter.py")
# foo = importlib.util.module_from_spec(spec)
# sys.modules["module.name"] = foo
# spec.loader.exec_module(foo)
module_name = 'parameter'

# # We can use importlib to import the module dynamically
module = importlib.import_module(module_name).CHECKPOINT_PATH

print(module)


# Output:
# 3.141592653589793
