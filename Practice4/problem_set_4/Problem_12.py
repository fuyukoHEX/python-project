import json
import sys

def diff(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())
        for key in keys:
            new_path = f"{path}.{key}" if path else key
            
            if key not in a:
                result.append(f"{new_path} : <missing> -> {json.dumps(b[key], separators=(',', ':'))}")
            elif key not in b:
                result.append(f"{new_path} : {json.dumps(a[key], separators=(',', ':'))} -> <missing>")
            else:
                diff(a[key], b[key], new_path)
    else:
        if a != b:
            result.append(f"{path} : {json.dumps(a, separators=(',', ':'))} -> {json.dumps(b, separators=(',', ':'))}")

a = json.loads(sys.stdin.readline())
b = json.loads(sys.stdin.readline())

result = []
diff(a, b)

if result:
    result.sort()
    print("\n".join(result))
else:
    print("No differences")