from testCamera import testCamera

class MarsSystem:
    def __init__(self):
        self.camera = testCamera()
        print "system init"

    def finalise(self):
        print "system finalize"
        
    def getCamera(self):
        return self.camera
        
if __name__ == "__main__":
    pass
