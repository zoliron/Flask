from netmiko import ConnectHandler


class Switch:
    def createSwitchDict(self, ip, username, password):
        SwitchDict = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password
        }
        return SwitchDict

    def sendCommand(self, SwitchDict, command):
        net_connect = ConnectHandler(**SwitchDict)
        output = net_connect.send_config_set(command)
        print(output)
        net_connect.disconnect()
        return output


if __name__ == '__main__':
    testSwitch = Switch()
    switchDict = testSwitch.createSwitchDict("192.168.200.254", "manager", "citizen")
    testSwitch.sendCommand(switchDict, "do show run int gi0/1")
