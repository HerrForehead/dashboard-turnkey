from pyVim import connect
import sys

# vSphere connection details
vcenter_hostname = 'vcenter.netlab.fhict.nl'
vcenter_user = 'PRO35@fhict.nl'
vcenter_pass = 'Wmy4CqMXY'

def print_network(network, level):
    indent = '  ' * level
    print(f"{indent}Network: {network.name}")

    # Check if the network has child folders
    if hasattr(network, 'childEntity'):
        # Retrieve and print the child folders
        child_folders = network.childEntity
        for child_folder in child_folders:
            print_network(child_folder, level + 1)

def retrieve_network_devices():
    try:
        # Connect to vSphere
        service_instance = connect.SmartConnect(
            host=vcenter_hostname,
            user=vcenter_user,
            pwd=vcenter_pass
        )

        # Retrieve the content
        content = service_instance.RetrieveContent()

        # Get the root folder
        root_folder = content.rootFolder

        # Retrieve all datacenters in the vSphere inventory
        datacenters = root_folder.childEntity
        for datacenter in datacenters:
            # Retrieve the network folder of the datacenter
            network_folder = datacenter.networkFolder

            # Retrieve the vDS-VLAN folder
            vds_vlan_folder = None
            for child_folder in network_folder.childEntity:
                if child_folder.name == 'vDS-VLAN':
                    vds_vlan_folder = child_folder
                    break

            # If vDS-VLAN folder is found, retrieve networks inside it
            if vds_vlan_folder:
                networks = vds_vlan_folder.childEntity
                for network in networks:
                    print_network(network, 0)

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Disconnect from vSphere
        connect.Disconnect(service_instance)

# Retrieve and display network devices
retrieve_network_devices()
