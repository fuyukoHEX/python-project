import json
import sys
import re

data = json.loads(sys.stdin.readline().strip())

q = int(sys.stdin.readline().strip())

for _ in range(q):
    query = sys.stdin.readline().strip()
    
    current = data
    found = True
    
    parts = query.split('.')
    
    for part in parts:
        matches = re.findall(r'([a-zA-Z_]\w*)|\[(\d+)\]', part)
        
        for name, index in matches:
            if name:
                if isinstance(current, dict) and name in current:
                    current = current[name]
                else:
                    found = False
                    break
            elif index:
                idx = int(index)
                if isinstance(current, list) and 0 <= idx < len(current):
                    current = current[idx]
                else:
                    found = False
                    break
        
        if not found:
            break
    
    if found:
        print(json.dumps(current, separators=(',', ':')))
    else:
        print("NOT_FOUND")