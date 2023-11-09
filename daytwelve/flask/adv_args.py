class User:
    def __init__(self,name):
        self.name = name
        self.logged_in = False

def auth_user(function):
    def wrapper(*args):
        if args[0].logged_in == True:
            function(args[0])
    return wrapper

@auth_user
def create_blog(user):
    print(f"The blog was created by {user.name}")


new_user = User("Jay")
new_user.logged_in = True
create_blog(new_user)

