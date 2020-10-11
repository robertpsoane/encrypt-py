## Button Functions for password manager

import webbrowser

class ButtonFunctions:
    def __init__(self,encryptor):
        self.encryptor = encryptor
    
    ## New File Function
    def newFile(self):
        pass

    ## Load File Function
    def loadFile(self):
        pass

    ## New Record Function
    def addRecord(self):
        pass

    ## Remove Record Function
    def removeRecord(self):
        pass

    ## Change Record Function
    def changeRecord(self):
        pass


    ## Show Help Function
    def helpButton(self):
        webbrowser.open("https://github.com/robertpsoane/encrypt-py")