from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim
import os

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE

si = SmartConnect(host='0.0.0.0', user='user', pwd='pass', port=443, sslContext=context)
atexit.register(Disconnect, si)
content = si.RetrieveContent()


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


def compile_folder_path_for_object(vobj):
    """ make a /vm/foo/bar/baz like folder path for an object """

    paths = []
    if isinstance(vobj, vim.Folder):
        paths.append(vobj.name)

    thisobj = vobj
    while hasattr(thisobj, 'parent'):
        thisobj = thisobj.parent
        if thisobj._moId == 'group-d1':
            break
        if isinstance(thisobj, vim.Folder):
            paths.append(thisobj.name)
    paths.reverse()
    return '/' + '/'.join(paths)

vm = get_obj(content, [vim.VirtualMachine], 'DC0_H0_VM0')

datacenter = 'DC0'

dc1 = get_obj(content, [vim.Datacenter], datacenter)
dcpath = compile_folder_path_for_object(dc1)
if not dcpath.endswith("/"):
    dcpath = dcpath + "/"
print('dcpath ' + dcpath)

#for folder in ['/', 'DC0', '/DC0', '/DC0/vm', '/vm', 'DC0/vm']:
for folder in ['/', 'F0', '/F0', '/F0/vm', '/vm', 'F0/vm']:
    if folder.startswith(dcpath + datacenter + '/vm'):
        print("First")
        fullpath = folder
    elif folder.startswith(dcpath + '/' + datacenter + '/vm'):
        print("Second")
        fullpath = folder
    elif folder.startswith('/vm/'):
        print("Third")
        fullpath = "%s%s%s" % (dcpath, datacenter, folder)
    elif folder == '/vm':
        print("Fourth")
        fullpath = "%s%s%s" % (dcpath, datacenter, folder)
    elif folder.startswith('/'):
        print("Fifth")
        fullpath = "%s%s/vm%s" % (dcpath, datacenter, folder)
    else:
        print("Sixth")
        fullpath = "%s%s/vm/%s" % (dcpath, datacenter, folder)

    print("%s => %s" % (folder, fullpath))
    fullpath = fullpath.rstrip('/')
    f_obj = content.searchIndex.FindByInventoryPath(fullpath)
    if f_obj:
        print("Found")
    print("*" * 80)
