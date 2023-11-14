import database

def profileIDChecker(netID):
    for i in database.get_freelancers():
        if i.get_netid() == netID:
            return True
    return False
    
if __name__ == '__main__':
    print(profileIDChecker('asdfgh'))
    print(profileIDChecker('hd0216'))