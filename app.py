import os
import threading
import subprocess
from pyVim import connect
from flask import Flask, render_template, request, redirect

# Add the networks to this list after retrieving them via retrieve_network_devices()
networkslist = []

# Add the username and password to this variable after logging in
username = ""
password = ""


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
                    #print(network.name)
                    networkslist.append(network.name)
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

@app.route('/result')
def result():
    return render_template("result.html")

# Grabs the data upon clicking the submit button and puts it in a dictionary
@app.route("/settings", methods=['POST', "GET"])
def settings():

    # Get the credentials from the form and put them in a dictionary
    usersettings = request.form.to_dict()

    print(usersettings)
    
    return render_template("configure.html")

# Grabs the data upon clicking the submit button and puts it in a dictionary
@app.route("/login", methods=['POST', "GET"])
def login():
    # Allow the username and password variables to be modified
    global username, password

    # Get the credentials from the form and put them in a dictionary
    credentials = request.form.to_dict()

    # Get the username and password from the credentials dictionary and put them in the global variables
    username = credentials['email']
    password = credentials['password']


    # Clear the networkslist to prevent duplicates when logging in again
    networkslist.clear()

    # Retrieve the networks and put them in the networkslist
    retrieve_network_devices(credentials['email'], credentials['password'])

    # Render the configure page with the list of networks as an option
    return render_template("configure.html", networks=networkslist)

# Renders the configure page
@app.route('/configure', methods=['GET', 'POST'])
def configure():
    if request.method == 'POST':

        # Get the username and print it
        print(username)

        # Get form data
        network = request.form.get('network')
        disk_space = request.form.get('disk_space')
        num_cores = request.form.get('num_cores')
        ram = request.form.get('ram')

        # Put the ansible command in a variable
        ansiblecommand = "ansible-playbook -i inventory.ini /home/student/turn-key-roll-out-playbooks/setupK8SVM.yml --extra-vars 'vm_net_name={network} vm_disk_gb={disk_space} vm_hw_cpu_n={num_cores} vm_hw_ram_mb={ram} vcenter_username={username} vcenter_password={password}'"

        # Run the ansible playbook using os.system and pass the form data as extra variables in a thread
        threading.Thread(target=os.system, args=(f'ansiblecommand="{ansiblecommand}"; /bin/bash -c "$ansiblecommand"',)).start()

        # Render the result page with the received data
        return render_template('result.html', disk_space=disk_space, num_cores=num_cores, ram=ram, network=network, username=username)
    


    # Render the configure page with the list of networks
    return render_template('configure.html')

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=('/home/student/dashboard-turn-key/cert.pem', '/home/student/dashboard-turn-key/key.pem'))

