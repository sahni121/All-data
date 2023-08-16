from listUser import allUser
from listGroup import allGroups
from permissionSet import permissionSet

allUser.list_users()
allGroups.list_groups()
# permissionSet.get_permission_set_details()
permissionSet.run_sso_permissions()