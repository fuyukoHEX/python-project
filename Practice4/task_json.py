import json

def print_interface_status(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    print("Interface Status")
    print("=" * 80)
    print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
    print(f"{'-'*50} {'-'*20} {'-'*7} {'-'*6}")
    
    for item in data['imdata']:
        attributes = item['l1PhysIf']['attributes']
        dn = attributes.get('dn', '')
        descr = attributes.get('descr', '')
        speed = attributes.get('speed', '')
        mtu = attributes.get('mtu', '')
        
        print(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<6}")

print_interface_status('sample-data.json')