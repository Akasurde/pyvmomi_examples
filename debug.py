from vm_lib import connect

fullpath = "/F0/DC0/vm/F0"
content = connect()
f_obj = content.searchIndex.FindByInventoryPath(fullpath)
print(f_obj)
