from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim
import os

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE

hostname = ''
username = ''
password = ''
template_name = ''

si = SmartConnect(host=hostname, user=username, pwd=password, port=443, sslContext=context)
atexit.register(Disconnect, si)
content = si.RetrieveContent()

def get_obj(content, vimtype, name=None):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    if name is None:
        obj = []
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj.append(c)
            break

    container.Destroy()
    return obj


vm = get_obj(content, [vim.VirtualMachine], template_name)
print(vm.summary.config.guestId)

