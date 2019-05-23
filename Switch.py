from netmiko import ConnectHandler


class Switch:
    def __init__(self, ip, username, password):
        self.SwitchDict = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }

    def sendCommand(self, command):
        try:
            net_connect = ConnectHandler(**self.SwitchDict)
        except:
            return "Switch Authentication Failed"
        output = net_connect.send_command(command, delay_factor=0.25)
        net_connect.disconnect()
        return output

    def sendCommandsList(self, command):
        try:
            net_connect = ConnectHandler(**self.SwitchDict)
        except:
            return "Switch Authentication Failed"
        output = net_connect.send_config_set("do " + command, delay_factor=0.25)
        net_connect.disconnect()
        return output
