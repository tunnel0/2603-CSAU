import yaml

def get_router_data():
    routers = []
    print("Ingrese los datos de los routers (escriba 'fin' en el IP para terminar):")
    
    while True:
        ip = input("Dirección IP de administración: ").strip()
        if ip.lower() == 'fin':
            break
        
        hostname = input("Hostname: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        routers.append({
            'ip': ip,
            'hostname': hostname,
            'username': username,
            'password': password
        })
    
    return routers

def main():
    routers = get_router_data()
    
    if routers:
        with open('routers_info.yaml', 'w') as file:
            yaml.dump(routers, file, default_flow_style=False, sort_keys=False)
        print(f"\nDatos guardados en routers_info.yaml ({len(routers)} routers).")
    else:
        print("\nNo se registraron datos.")

if __name__ == "__main__":
    main()
