import os

class Duh():

    # this changes source code
    ll = []
    
    def __init__(self) -> None:
        # this won't
        self.l = []

if __name__ == "__main__":
    os.system('clear')

    a = [1,2]
    b = [[3,4],[5,6]]

    res = [ a + j for j in b]
    print(res)