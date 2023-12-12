import database

def profileIDChecker(netID):
    return database.is_visible(netID)
    
if __name__ == '__main__':
    print(profileIDChecker('asdfgh'))
    print(profileIDChecker('hd0216'))