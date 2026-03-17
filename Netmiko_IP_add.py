import yaml
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException

def load_routers(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def configure_router(router_info):
    device = {
        'device_type': 'cisco_xe',
        'host': router_info['ip'],
        'username': router_info['username'],
        'password': router_info['password'],
    }
    
    if 'interfaces' not in router_info:
        print(f"No se encontraron interfaces para {router_info['hostname']}")
        return

    config_commands = []
    for interface in router_info['interfaces']:
        config_commands.extend([
            f"interface {interface['name']}",
            f"ip address {interface['ip']} {interface['mask']}",
            "no shutdown"
        ])
    
    print(f"\n>>> Conectando a {router_info['hostname']} ({router_info['ip']})...")
    try:
        with ConnectHandler(**device) as net_connect:
            print(f"Aplicando configuración de {len(router_info['interfaces'])} interfaz(ces)...")
            output = net_connect.send_config_set(config_commands)
            print(output)
            
            print("Guardando configuración...")
            net_connect.send_command("write memory")
            print(f"Configuración completada exitosamente en {router_info['hostname']}.")
                
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        print(f"Error de conexión en {router_info['hostname']}: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado en {router_info['hostname']}: {e}")

def main():
    try:
        routers = load_routers('routers_info.yaml')
        if not routers:
            print("No se encontraron routers en routers_info.yaml")
            return
            
        for router in routers:
            configure_router(router)
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo routers_info.yaml")

if __name__ == "__main__":
    main()
