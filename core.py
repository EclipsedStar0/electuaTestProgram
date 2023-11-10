import infoCodex
import guidisplay

# noinspection PyPep8Naming
class Core:
    def __init__(self):
        self.infoCodex = infoCodex.InfoCodex()
        self.display = guidisplay.Display()
        self.programActive = True

        self.runtime()

    def runtime(self):
        while self.programActive:
            self.timeStep()

    def timeStep(self):
        self.display.generateDisplay()
