import sys
import time

import pygame
import pygame.freetype
import pygame.mixer
import random


# noinspection PyPep8Naming
class Display:
    def __init__(self):
        self.displayData = dict()
        self.width, self.height = 1024, 576
        self.pygameColorCodes = {
            "Blue": (0, 0, 255),
            "Cyan": (10, 230, 240),
            "Green Cyan": (10, 240, 200),
            "Bright Cyan Green": (10, 250, 230),
            "Green": (0, 255, 0),
            "Lime Green": (50, 200, 50),
            "Fern": (100, 180, 100),
            "Reseda Green": (110, 130, 90),
            "Dark Green": (0, 100, 0),
            "Light Red": (180, 0, 0),
            "Red": (255, 0, 0),
            "Dull Orange": (220, 100, 0),
            "Orange": (255, 140, 0),
            "Bright Orange": (255, 190, 20),
            "Purple": (100, 30, 125),
            "Yellow": (230, 230, 0),
            "White": (240, 240, 240),
            "Light Gray": (60, 60, 60),
            "Dark Gray": (45, 45, 45),
            "Darker Gray": (30, 30, 30),
            "Light Black": (10, 10, 10),
            "Brown": (150, 75, 0),
            "Light Brown": (200, 160, 130)
        }


        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.set_caption("Unsecure Terminal")
        self.CLOCK = pygame.time.Clock()
        self.FONT = pygame.freetype.Font("fonts/luximr.ttf", 14)
        self.fontspace = 0.0076086956
        self.smallFont = pygame.freetype.Font("fonts/luximr.ttf", 12)
        self.extraSmallFont = pygame.freetype.Font("fonts/luximr.ttf", 10)
        self.specialFont = pygame.freetype.SysFont("mvboli", 28)
        self.SCREEN = pygame.display.set_mode((self.width, self.height))
        self.SCREEN.fill((0, 0, 0))

        proxBlockSize = 2
        rangeModifier = 1.5
        for currentRow in range(int(self.height / proxBlockSize)):
            for currentColumn in range(int(self.width / proxBlockSize)):
                randList = sorted([rangeModifier * random.randint(2, 5), rangeModifier * random.randint(2, 5), rangeModifier * random.randint(4, 8)], reverse=True)
                pygame.draw.rect(self.SCREEN, (randList[0] - 1 * rangeModifier, randList[1], randList[2] + 3 * rangeModifier), (int(currentColumn * proxBlockSize - proxBlockSize), int(currentRow * proxBlockSize - proxBlockSize), proxBlockSize, proxBlockSize))
        pygame.display.update()
        pygame.image.save(self.SCREEN, "screenholder/mainBackground.png")
        self.backgroundIMG = pygame.image.load("screenholder/mainBackground.png").convert_alpha()

        self.blueOverlayTint = pygame.Surface((self.width * 0.65, self.height * 0.6), pygame.SRCALPHA)

        # Go 0, 40, 180
        self.blueOverlayTint.fill((180, 40, 0, 4))
        # self.SCREEN.blit(self.blueOverlayTint, (int(self.width*0.2), int(self.height*0.175)))

        pygame.mouse.set_visible(False)

    def typeWriterFormat(self, string, color, mode=False):
        subSurface = dict()
        strUpToNow = ""
        index = 0
        for char in string:
            strUpToNow += char
            subSurf = pygame.Surface(((self.width * (index + 1) * self.fontspace * 1.05), self.height * 0.025))
            self.FONT.render_to(subSurf, (0, 0), strUpToNow, color)
            subSurface[index] = subSurf
            index += 1
        if mode:
            increaseTime = [2, 4, 7]
            for holder in range(0, 16):
                if holder in increaseTime:
                    strUpToNow += "."
                subSurf = pygame.Surface(((self.width * (index + 1) * self.fontspace * 1.05), self.height * 0.025))
                self.FONT.render_to(subSurf, (0, 0), strUpToNow, color)
                subSurface[index] = subSurf
                index += 1
        return subSurface

    def fakeSleep(self, fakeTime):
        fakeTime += time.time()
        while time.time() < fakeTime:
            # print(startTime, desigTime)
            # Catch User Events just incase, so we don't get blue glowing circle; We won't actually be processing events here
            for userEvent in pygame.event.get():
                if userEvent.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.CLOCK.tick(240)

    def generateDisplay(self, menu="Main"):
        self.SCREEN.blit(self.backgroundIMG, (0, 0))
        if menu == "Main":
            self.SCREEN.blit(self.blueOverlayTint, (int(self.width*0.2), int(self.height*0.175)))

            typeStr = "Terminal Powering On"
            index = 0
            updateTime = 1/30
            variance = 0.15
            subSurface = self.typeWriterFormat(typeStr, self.pygameColorCodes.get("Light Gray"), True)
            copiedSurf = self.SCREEN.copy()
            for index in subSurface:
                desigTime = time.time() + updateTime + random.randint(int(variance * -100), int(variance * 100)) / 100 * updateTime
                self.SCREEN.blit(copiedSurf, (0, 0))
                self.SCREEN.blit(subSurface.get(index), (self.width * 0.4125, self.height * 0.25))
                pygame.display.update()
                while time.time() < desigTime:
                    # print(startTime, desigTime)
                    # Catch User Events just incase, so we don't get blue glowing circle; We won't actually be processing events here
                    for userEvent in pygame.event.get():
                        if userEvent.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    self.CLOCK.tick(240)
            self.fakeSleep(10)

            # self.FONT.render_to(self.SCREEN, (self.width*0.4125, self.height*0.25), "Terminal Powering On", (self.pygameColorCodes.get("Light Gray")))
            # pygame.draw.rect(self.SCREEN, (255, 0, 0), (self.width * 0.525, 0, 2, self.height))
            # 0.525 - 0.35 = 0.175 / 23 = 0.00760869565; Each char needs 0.0076 width
            pygame.display.update()

        else:
            pass

    def getDisplayData(self):
        return self.displayData
