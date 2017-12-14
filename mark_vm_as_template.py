from pyVmomi import vim
from vm_lib import get_obj, connect

content = connect()

vm = get_obj(content, [vim.VirtualMachine], 'DC0_H0_VM0')
vm.MarkAsTemplate()
