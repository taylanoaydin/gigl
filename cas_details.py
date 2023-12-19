import requests
from req_lib import ReqLib

#Returns a list of lists of the following information:
#   [0] displayname (Name+Surname)
#   [1] sn (Surname)
#   [2] mail
#   [3] department
#   [4] pustatus
#   [5] eduPersonPrimaryAffiliation
#   [6] universityid
def cas_details(netID):
    req_lib = ReqLib()
    req = req_lib.getJSON(
        req_lib.configs.USERS,
        uid=netID,
    )
    info_list = [[item['displayname']] for item in req]
    return info_list[0]

#Test
if __name__ == '__main__':
    print(cas_details('ogolev2'))
