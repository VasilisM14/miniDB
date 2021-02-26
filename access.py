from functools import wraps

def AccessEn(reqPriv, curPriv):

    if reqPriv == "master" and curPriv == "master" :
        return True

    if reqPriv == "admin" and (curPriv =="master" or curPriv=="master"):
        return True

    if reqPriv == "user":
        return True

    return False    

def privaccess(reqPriv):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            self = args[0]

            if self._isnew:
                ret = function(*args, **kwargs) 
                return ret

            currentUser = self.currentUser

            tables = currentUser.tables[0]

            if not hasAccess(reqPriv,currentUser.group[0].strip()):
                raise Exception('User Access Denied ')

            if currentUser.group[0] == "master":
                ret = function(*args, **kwargs) 
                return ret

            if tables != "*":
                for table in tables.split(","):
                    if table == args[1]:
                        ret = function(*args, **kwargs) 
                        return ret
                raise Exception('Table Access Denied')
            else:
                if not args[1][:4]=="meta":
                    ret = function(*args, **kwargs) 
                    return ret
                else:
                    raise Exception('Access Denied')

        return wrapper
    return real_decorator