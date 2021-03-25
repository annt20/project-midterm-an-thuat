from netmiko import ConnectHandler

user = int(input('Which switch do you want to configure?\n\t(1) 192.168.1.2 (core switch)'
                 '\n\t(2) 192.168.1.3 (switch 1)'
                 '\n\t(3) 192.168.1.4 (switch 2)'
                 '\n\tPlease enter 1, 2 or 3:'))
vlan_file = int(input('Which vlan file do you want to input?'
                      '\n\t(1). "core_switch_vlan.csv"'
                      '\n\t(2). "switch2_vlan.csv"'
                      '\n\t(3). "switch3_vlan.csv"'
                      '\n\tPlease enter 1, 2 or 3:'))

if user == 1:
    ip_address = '192.168.1.2'
    print('Configuring ', ip_address, '..... using file core_switch_vlan.csv.......')
    # ssh_name = input('Enter ssh username: ')
    # ssh_password = input('Enter ssh password: ')
    my_switch1 = {
        'device_type': 'cisco_ios',
        'ip': ip_address,
        'username': 'en',
        'password': 'en',
        'secret': 'en'  # secret default '' (no set enable secret)
    }
    switch1_connect = ConnectHandler(**my_switch1)
    switch1_connect.enable()
    command = 'terminal length 0'
    output = switch1_connect.send_command(command)
    print(output)
    interface1_trunk_mode = ['int g0/1', 'switchport trunk encapsulation dot1q', 'switchport mode trunk', 'exit']
    interface2_trunk_mode = ['int g0/2', 'switchport trunk encapsulation dot1q', 'switchport mode trunk', 'exit']
    output = switch1_connect.send_config_set(interface1_trunk_mode, interface2_trunk_mode)
    print(output)
    output = switch1_connect.send_config_set('ip routing')
    print(output)
    f = open('core_switch_vlan.csv', 'r')
    line = f.readline()
    line = f.readline()
    while line != '':
        elements = line.split(',')
        vlan = elements[5]
        vlan_name = 'name ' + elements[1]
        interface_vlan = 'int vlan ' + elements[0]
        ip_address_command = 'ip address ' + elements[2] + ' ' + elements[3]
        exit_cmd = 'exit'
        dhcp_pool = 'ip dhcp pool ' + elements[1]
        network_vlan = 'network ' + elements[4] + " " + elements[3]
        def_rou = 'default-router ' + elements[2]
        vlan_config_commands = [vlan, vlan_name, interface_vlan, ip_address_command, exit_cmd, dhcp_pool, network_vlan, def_rou]
        output = switch1_connect.send_config_set(vlan_config_commands)
        print(output)
        line = f.readline()
elif user == 2:
    ip_address = '192.168.1.3'
    print('Configuring ', ip_address, '..... using file switch2_vlan.csv.......')

    my_switch2 = {
        'device_type': 'cisco_ios',
        'ip': ip_address,
        'username': 'en',
        'password': 'en',
        'secret': 'en'  # secret default '' (no set enable secret)
    }
    ssh_connect2 = ConnectHandler(**my_switch2)
    ssh_connect2.enable()
    ssh_connect2.send_command('terminal length 0')
    ssh_connect2.send_config_set('hostname S1')
    interface_g00_configuring = ['interface g0/1', 'switchport trunk encapsulation dot1q',
                                 'switchport mode trunk', 'exit']
    output = ssh_connect2.send_config_set(interface_g00_configuring)
    print(output)
    f = open('switch2_vlan.csv', 'r')
    line = f.readline()
    line = f.readline()
    while line != '':
        elements = line.split(',')
        vlan = 'vlan ' + elements[0]
        vlan_name = 'name ' + elements[1]
        vlan_access = []
        if len(line) > 43 and len(elements[5]) >= 4:
            interface_g = 'interface ' + elements[5].strip()
            switchport = 'switchport mode access'
            set_vlan_access =  'switchport access vlan ' + elements[0]
            vlan_access = [vlan, vlan_name, interface_g, switchport, set_vlan_access]
        else:
            vlan_access = [vlan, vlan_name]
        output = ssh_connect2.send_config_set(vlan_access)
        print(output)
        line = f.readline()
    ssh_connect2.disconnect()
else:
    ip_address = '192.168.1.4'
    print('Configuring ', ip_address, '..... using file switch2_vlan.csv.......')
    # ssh_name = input('Enter ssh username: ')
    # ssh_password = input('Enter ssh password: ')
    my_switch3 = {
        'device_type': 'cisco_ios',
        'ip': ip_address,
        'username': 'en',
        'password': 'en',
        'secret': 'en'  # secret default '' (no set enable secret)
    }
    ssh_connect2 = ConnectHandler(**my_switch3)
    ssh_connect2.enable()
    ssh_connect2.send_command('terminal length 0')
    # ssh_connect2.send_config_set('hostname S2')
    interface_g00_configuring = ['interface g0/1', 'switchport trunk encapsulation dot1q',
                                 'switchport mode trunk', 'exit']
    output = ssh_connect2.send_config_set(interface_g00_configuring)
    print(output)
    f = open('switch3_vlan.csv', 'r')
    line = f.readline()
    line = f.readline()
    while line != '':

        elements = line.split(',')
        vlan = 'vlan ' + elements[0]
        vlan_name = 'name ' + elements[1]
        vlan_access = []
        if len(line) > 43 and len(elements[5]) >= 4:

            interface_g = 'interface ' + elements[5].strip()
            switchport = 'switchport mode access'
            set_vlan_access = 'switchport access vlan ' + elements[0]
            vlan_access = [vlan, vlan_name, interface_g, switchport, set_vlan_access]
        else:
            vlan_access = [vlan, vlan_name]
        output = ssh_connect2.send_config_set(vlan_access)
        print(output)
        line = f.readline()
    ssh_connect2.disconnect()