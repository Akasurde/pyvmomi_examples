from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim, vmodl
import time

def connect(hostname, username, password):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=hostname, user=username, pwd=password, port=443, sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    return content

hostname = ""
username = "administrator@vsphere.local"
password = ""
role_name = 'RP administrator'

content = connect(hostname, username, password)
auth_mgr = content.authorizationManager

print([ role.privilege for role in auth_mgr.roleList if role.name == role_name ])
