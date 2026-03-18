import requests
import yaml
import time
import json
import urllib3
import os

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONFIG_FILE = 'routers_info.yaml'
STATUS_FILE = 'status.json'

def get_interface_status(ip, username, password, interface_name):
    url = f"https://{ip}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface={interface_name}"
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }
    try:
        response = requests.get(
            url,
            auth=(username, password),
            headers=headers,
            verify=False,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if_data = data.get('Cisco-IOS-XE-interfaces-oper:interface', {})
            return {
                "name": interface_name,
                "admin_status": if_data.get('admin-status', 'N/A'),
                "oper_status": if_data.get('oper-status', 'N/A'),
                "last_change": if_data.get('last-change', 'N/A')
            }
        else:
            return {"name": interface_name, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"name": interface_name, "error": str(e)}

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found.")
        return

    while True:
        with open(CONFIG_FILE, 'r') as f:
            routers = yaml.safe_load(f)

        all_status = []
        for router in routers:
            router_status = {
                "hostname": router['hostname'],
                "ip": router['ip'],
                "interfaces": []
            }
            # The prompt says G1 and G2, but the YAML has G2 and G3.
            # I'll use the ones in the YAML.
            for iface in router.get('interfaces', []):
                iface_name = iface['name']
                status = get_interface_status(router['ip'], router['username'], router['password'], iface_name)
                router_status['interfaces'].append(status)
            
            all_status.append(router_status)

        with open(STATUS_FILE, 'w') as f:
            json.dump(all_status, f, indent=4)
        
        print(f"Updated status at {time.ctime()}")
        time.sleep(5)

if __name__ == "__main__":
    main()
