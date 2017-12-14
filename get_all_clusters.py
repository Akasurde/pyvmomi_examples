#!/usr/bin/env python
"""
List Of Hosts in a Cluster
"""
from vm_lib import connect, get_obj
from pyVmomi import vim

def main():
    content = connect()
    cluster_name = 'DC0_C0'
    for cluster_obj in get_obj(content, vim.ComputeResource,
            cluster_name):
        if cluster_name:
            if cluster_obj.name == cluster_name:
                for host in cluster_obj.host:
                    print host.name
        else:
            print cluster_obj.name


# start this thing
if __name__ == "__main__":
    main()
