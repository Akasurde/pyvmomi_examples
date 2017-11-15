from pyVmomi import vmodl

try:
    raise vmodl.fault.InvalidRequest
except vmodl.fault.InvalidRequest as e:
    print(e.msg)
