import yaml
from ncclient import manager
import xml.dom.minidom
import xmltodict

def get_netconf_interfaces(router):
    try:
        with manager.connect(
            host=router['ip'],
            port=830,
            username=router['username'],
            password=router['password'],
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
            # Try Cisco-native operational model for IOS-XE
            # Namespace: http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper
            netconf_filter = """
              <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
                <interface/>
              </interfaces>
            """
            interface_info = m.get(filter=('subtree', netconf_filter))
            return interface_info.xml
    except Exception as e:
        return f"Error connecting to {router['hostname']}: {e}"

def main():
    with open('routers_info.yaml', 'r') as f:
        routers = yaml.safe_load(f)

    for router in routers:
        print(f"\n--- Interface Status for {router['hostname']} ({router['ip']}) ---")
        xml_data = get_netconf_interfaces(router)
        
        if "Error" in xml_data:
            print(xml_data)
        else:
            data_dict = xmltodict.parse(xml_data)
            try:
                # Actualizar el path para el modelo nativo de Cisco
                interfaces = data_dict.get('rpc-reply', {}).get('data', {}).get('interfaces', {}).get('interface', [])
                
                if not interfaces:
                    print("No se encontraron interfaces con el modelo nativo.")
                    continue

                if isinstance(interfaces, dict):
                    interfaces = [interfaces]

                print(f"{'Interface Name':<25} {'Admin Status':<15} {'Oper Status':<15}")
                print("-" * 55)
                for iface in interfaces:
                    name = iface.get('name')
                    # En el modelo nativo los campos pueden ser 'admin-status' o similares
                    admin_status = iface.get('admin-status', 'N/A')
                    oper_status = iface.get('oper-status', 'N/A')
                    print(f"{name:<25} {admin_status:<15} {oper_status:<15}")
            except Exception as e:
                print(f"Error procesando XML o el modelo no es soportado: {e}")

if __name__ == "__main__":
    main()
