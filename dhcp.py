import yaml
from netmiko import ConnectHandler
import os

def get_network(ip, mask):
    """Simple network calculation for /24 masks common in this lab."""
    if mask == "255.255.255.0":
        octets = ip.split('.')
        return f"{octets[0]}.{octets[1]}.{octets[2]}.0"
    return "0.0.0.0" # Fallback or more complex logic could go here

def configure_dhcp():
    file_path = '/home/juan/2603-CSAU/routers_info.yaml'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r') as f:
        routers = yaml.safe_load(f)

    for r_data in routers:
        hostname = r_data.get('hostname')
        if hostname not in ['R1', 'R2']:
            continue
            
        # Find GigabitEthernet3
        g3 = next((i for i in r_data.get('interfaces', []) if 'GigabitEthernet3' in i['name']), None)
        
        if not g3:
            print(f"Interface G3 not found for {hostname}")
            continue

        gw_ip = g3['ip']
        mask = g3['mask']
        network = get_network(gw_ip, mask)
        
        device = {
            'device_type': 'cisco_ios',
            'host': r_data['ip'],
            'username': r_data['username'],
            'password': r_data['password'],
        }

        print(f"\n>>> Configuring DHCP on {hostname} ({device['host']})")
        try:
            with ConnectHandler(**device) as net_connect:
                commands = [
                    f"ip dhcp excluded-address {gw_ip}",
                    f"ip dhcp pool POOL_LAN_G3",
                    f"network {network} {mask}",
                    f"default-router {gw_ip}",
                    f"dns-server 8.8.8.8 1.1.1.1"
                ]
                output = net_connect.send_config_set(commands)
                print(output)
                net_connect.save_config()
                print(f"Configuration saved for {hostname}")
        except Exception as e:
            print(f"Error connecting to {hostname}: {e}")

if __name__ == "__main__":
    configure_dhcp()
