import importlib

q = int(input())

for _ in range(q):
    module_path, attribute = input().split()
    try:
        mod = importlib.import_module(module_path)
    except ImportError:
        print("MODULE_NOT_FOUND")
        continue
    if hasattr(mod, attribute):
        attr_val = getattr(mod, attribute)

        if callable(attr_val):
            print("CALLABLE")
        else:
            print("VALUE")
    else:
        print("ATTRIBUTE_NOT_FOUND")