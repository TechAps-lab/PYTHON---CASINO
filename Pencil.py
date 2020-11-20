class Pencil:
        
    def printFail(self, string): print("\033[91m {}\033[00m ".format(string))

    def printWin(self, string): print("\033[92m {}\033[00m ".format(string))

    def printWarning(self, string): print("\033[93m {}\033[00m ".format(string))
