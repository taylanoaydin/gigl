import requests

bearer_token = 'OWU1NGY4ZGEtY2EyMi0zYTZiLWE2ZjMtNzYxM2NlODVkZWUxOmhkMDIxNkBjYXJib24uc3VwZXI='
#Returns a list of lists of the following information:
#   [0] displayname (Name+Surname)
#   [1] sn (Surname)
#   [2] mail
#   [3] department
#   [4] pustatus
#   [5] eduPersonPrimaryAffiliation
#   [6] universityid
def cas_details(netID):
    my_headers = {'Authorization' : 'Bearer {access_token}'.format(access_token=bearer_token),
                  'Accept' : 'application/json'}
    response = requests.get('https://api.princeton.edu:443/active-directory/1.0.5/users?uid='+(netID), headers=my_headers)
    info_list = [[item['displayname'],
                  item['sn'],
                  item['mail'],
                  item['department'],
                  item['pustatus'],
                  item['eduPersonPrimaryAffiliation'],
                  item['universityid']] for item in response.json()]
    return info_list[0]

#Test
if __name__ == '__main__':
    print(cas_details('hd0216'))
    print(cas_details('ta0639'))