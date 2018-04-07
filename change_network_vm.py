import atexit
import argparse
import sys
import time
import ssl
import os
from pyVmomi import vim, vmodl
from pyVim.connect import Disconnect, SmartConnect

inputs = {
    'vcenter_ip': '',
    'vcenter_password': '',
    'vcenter_user': '',
    'vm_name': '',
    'isDHCP': False,
    'vm_ip': '',
    'subnet': '',
    'gateway': '',
    'dns': ['8.8.8.8', '1.1.1.1'],
    'domain': 'domain.com'
}


def connect_to_api():
    hostname = inputs['vcenter_ip']
    username = inputs['vcenter_user']
    password = inputs['vcenter_password']
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=hostname, user=username,
                      pwd=password, port=443, sslContext=context)
    atexit.register(Disconnect, si)
    return si.RetrieveContent()


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    container.Destroy()
    return obj


def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """
    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)
    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            print('%s completed successfully, result: %s' %
                  (actionName, task.info.result))
        else:
            print('%s completed successfully.' % actionName)
    else:
        print('%s did not complete successfully: %s' %
              (actionName, task.info.error))
        raise task.info.error
    return task.info.result


def main():
    try:
        print("Connected to VCENTER SERVER !")
        content = connect_to_api()
        vm_name = inputs['vm_name']
        vm = get_obj(content, [vim.VirtualMachine], vm_name)

        if vm.runtime.powerState != 'poweredOff':
            sys.exit("WARNING:: Power off your VM before reconfigure")

        adaptermap = vim.vm.customization.AdapterMapping()
        globalip = vim.vm.customization.GlobalIPSettings()
        adaptermap.adapter = vim.vm.customization.IPSettings()
        isDHDCP = inputs['isDHCP']
        if not isDHDCP:
            """Static IP Configuration"""
            adaptermap.adapter.ip = vim.vm.customization.FixedIp()
            adaptermap.adapter.ip.ipAddress = inputs['vm_ip']
            adaptermap.adapter.subnetMask = inputs['subnet']
            adaptermap.adapter.gateway = inputs['gateway']
            globalip.dnsServerList = inputs['dns']
        else:
            """DHCP Configuration"""
            adaptermap.adapter.ip = vim.vm.customization.DhcpIpGenerator()

        adaptermap.adapter.dnsDomain = inputs['domain']

        globalip = vim.vm.customization.GlobalIPSettings()

        ident = vim.vm.customization.LinuxPrep(
            domain=inputs['domain'], hostName=vim.vm.customization.FixedName(name=vm_name))
        customspec = vim.vm.customization.Specification()
        # For only one adapter
        customspec.identity = ident
        customspec.nicSettingMap = [adaptermap]
        customspec.globalIPSettings = globalip

        # Configuring network for a single NIC
        # For multipple NIC configuration contact me.

        print("Reconfiguring VM Networks...")

        task = vm.Customize(spec=customspec)

        # Wait for Network Reconfigure to complete
        wait_for_task(task, si)

    except vmodl.MethodFault, e:
        print("Caught vmodl fault: %s" % e.msg)
        return 1
    except Exception, e:
        print("Caught exception: %s" % str(e))
        return 1

# Start program
if __name__ == "__main__":
    main()
