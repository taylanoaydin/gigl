import database

def profileIDChecker(netID):
    ls, _ = database.get_freelancers()
    for i in ls:
        if i.get_netid() == netID:
            return True
    return False
    
if __name__ == '__main__':
    print(profileIDChecker('asdfgh'))
    print(profileIDChecker('hd0216'))