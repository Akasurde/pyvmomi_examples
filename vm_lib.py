from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim

def connect():
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host='0.0.0.0', user='user', pwd='pass', port=443, sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    return content

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
