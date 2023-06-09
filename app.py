import os
import threading
import subprocess
from pyVim import connect
from flask import Flask, render_template, request, redirect

def print_network(network, level):
    indent = '  ' * level
    print(f"{indent}Network: {network.name}")

    # Check if the network has child folders
    if hasattr(network, 'childEntity'):
        # Retrieve and print the child folders
        child_folders = network.childEntity
        for child_folder in child_folders:
            print_network(child_folder, level + 1)

def retrieve_network_devices(username, password):
    try:
        # Connect to vSphere
        service_instance = connect.SmartConnect(
            host="vcenter.netlab.fhict.nl",
            user=username,
            pwd=password
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

# Create the app
app = Flask(__name__)

# Force redirect to HTTPS
@app.before_request
def force_https():
    if request.endpoint in app.view_functions and not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'))


# Renders the home page
@app.route('/')
def start():
    return render_template("login.html")

# Renders the home page
@app.route('/home')
def home():
    return render_template("login.html")

# Grabs the data upon clicking the submit button and puts it in a dictionary
@app.route("/settings", methods=['POST', "GET"])
def result():
    settings = request.form.to_dict()
    print(settings)
    return render_template("configure.html")


@app.route("/login", methods=['POST', "GET"])
def login():
    credentials = request.form.to_dict()
    print(credentials)

    retrieve_network_devices(credentials['email'], credentials['password'])


    return render_template("configure.html")

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=('/home/student/dashboard-turn-key/cert.pem', '/home/student/dashboard-turn-key/key.pem'))

