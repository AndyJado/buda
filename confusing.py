import os

class Duh():

    # this changes source code
    ll = []
    
    def __init__(self) -> None:
        # this won't
        self.l = []

if __name__ == "__main__":
    os.system('clear')
    duh = Duh()
    duh2 = Duh()
    duh.ll.append(2)
    print(duh2.ll)