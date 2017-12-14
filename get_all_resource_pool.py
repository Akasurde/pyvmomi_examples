from vm_lib import connect, get_obj

content = connect()

def obj_has_parent(obj, parent):
    if obj is None and parent is None:
        raise AssertionError()
    current_parent = obj

    moid = current_parent._moId
    while True: #moid not in ['group-d1', 'ha-folder-root']:
        if current_parent.name == parent.name:
            return True
        moid = current_parent._moId 
        if moid in ['group-d1', 'ha-folder-root']:
            return False

        current_parent = current_parent.parent
        if current_parent is None:
            return False

def select_resource_pool_by_host(host, rp):
        # Find resource pool on host
        print(host.parent.name)
        if obj_has_parent(rp[0].parent, host.parent):
			return rp[0].name

host_name = sys.argv[1]
rp = sys.argv[2]
hosts = get_obj(content, [vim.HostSystem], host_name)
rep = get_obj(content, [vim.ResourcePool], rp)
print select_resource_pool_by_host(hosts, [rep])
