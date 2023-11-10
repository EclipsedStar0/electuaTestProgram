import math
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
        self.monitorRefreshRate = 239
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
                pygame.draw.rect(self.SCREEN, (int(randList[0] - 1 * rangeModifier), int(randList[1]), int(randList[2] + 3 * rangeModifier)), (int(currentColumn * proxBlockSize - proxBlockSize), int(currentRow * proxBlockSize - proxBlockSize), proxBlockSize, proxBlockSize))
        pygame.display.update()
        pygame.image.save(self.SCREEN, "screenholder/mainBackground.png")
        self.backgroundIMG = pygame.image.load("screenholder/mainBackground.png").convert_alpha()
        self.overlayTint = pygame.Surface((self.width * 0.65, self.height * 0.6), pygame.SRCALPHA)

        # Go 0, 40, 180
        self.overlayTint.fill((180, 40, 0, 4))
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
            for holder in range(0, increaseTime[-1]+1):
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
            self.CLOCK.tick(self.monitorRefreshRate)

    def generateDisplay(self, menu="Main"):
        self.SCREEN.blit(self.backgroundIMG, (0, 0))
        if menu == "Main":
            self.SCREEN.blit(self.overlayTint, (int(self.width*0.2), int(self.height*0.175)))

            """ This section draws the designated string """
            typeStr = "Terminal Powering On"
            updateTime = 1/30
            variance = 0.15
            subSurface = self.typeWriterFormat(typeStr, self.pygameColorCodes.get("Light Gray"), True)
            copiedSurf = self.SCREEN.copy()
            indexArr = []
            progressBarPercent = 0
            for index in subSurface:
                indexArr.append(index)
            for index in range(0, len(indexArr)):
                desigTime = time.time() + updateTime + random.randint(int(variance * -100), int(variance * 100)) / 100 * updateTime
                if index == len(typeStr):
                    # Now we can draw in the progress bar
                    pygame.draw.rect(copiedSurf, (60, 10, 0), (self.width * 0.25, self.height * 0.35, self.width * 0.5, self.height * 0.035), int(self.width * 0.004))
                elif index > len(typeStr):
                    # Most it can go up at this stage is 5% at a time
                    progressBarPercent += random.randint(0, 250)/10000
                    pygame.draw.rect(copiedSurf, (120, 30, 0), (self.width * 0.25 + int(self.width * 0.004), self.height * 0.35 + int(self.width * 0.004), (self.width * 0.5 - int(self.width * 0.004) * 2) * progressBarPercent, self.height * 0.035 - int(self.width * 0.004) * 2))
                self.SCREEN.blit(copiedSurf, (0, 0))
                self.SCREEN.blit(subSurface.get(indexArr[index]), (self.width * 0.4125, self.height * 0.25))
                pygame.display.update()
                while time.time() < desigTime:
                    # print(startTime, desigTime)
                    # Catch User Events just incase, so we don't get blue glowing circle; We won't actually be processing events here
                    for userEvent in pygame.event.get():
                        if userEvent.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    self.CLOCK.tick(self.monitorRefreshRate)

            """ This section draws the '...' expanding and then retracting """
            cycleTimes = random.randint(3, 9)
            updateTime *= 1.5
            variance *= 1.25

            numCycles = 0
            while progressBarPercent != 1:
                numCycles += 1
                print(numCycles, progressBarPercent)
                self.fakeSleep(random.randint(1, 3) * random.randint(20, 40)/100)
                rewindTime = updateTime * 2
                for index in range(len(indexArr) - 1, len(typeStr), -1):
                    desigTime = time.time() + rewindTime + random.randint(int(variance * -100), int(variance * 100)) / 100 * rewindTime
                    interval = 200
                    if progressBarPercent < 0.27:
                        interval /= 4
                    elif progressBarPercent < 0.95:
                        interval = abs(math.sin(numCycles/2)) * interval
                    else:
                        interval /= 80
                    progressBarPercent += random.randint(int(pow(numCycles, 1.7)), max(int(interval + pow(numCycles, 2)), int(pow(numCycles + 3, 1.7))))/10000
                    progressBarPercent = min(progressBarPercent, 1)
                    pygame.draw.rect(copiedSurf, (120, 30, 0), (self.width * 0.25 + int(self.width * 0.004), self.height * 0.35 + int(self.width * 0.004), (self.width * 0.5 - int(self.width * 0.004) * 2) * progressBarPercent, self.height * 0.035 - int(self.width * 0.004) * 2))
                    self.SCREEN.blit(copiedSurf, (0, 0))
                    self.SCREEN.blit(subSurface.get(indexArr[index]), (self.width * 0.4125, self.height * 0.25))
                    pygame.display.update()
                    while time.time() < desigTime:
                        # print(startTime, desigTime)
                        # Catch User Events just incase, so we don't get blue glowing circle; We won't actually be processing events here
                        for userEvent in pygame.event.get():
                            if userEvent.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        self.CLOCK.tick(self.monitorRefreshRate)
                for index in range(len(typeStr)-1, len(indexArr)):
                    desigTime = time.time() + updateTime + random.randint(int(variance * -100), int(variance * 100)) / 100 * updateTime
                    interval = 200
                    if progressBarPercent < 0.27:
                        interval /= 4
                    elif progressBarPercent < 0.95:
                        interval = abs(math.sin(numCycles/2)) * interval
                    else:
                        interval /= 80
                    progressBarPercent += random.randint(int(pow(numCycles, 1.7)), max(int(interval + pow(numCycles, 2)), int(pow(3 + numCycles, 1.7))))/10000
                    progressBarPercent = min(progressBarPercent, 1)
                    pygame.draw.rect(copiedSurf, (120, 30, 0), (self.width * 0.25 + int(self.width * 0.004), self.height * 0.35 + int(self.width * 0.004), (self.width * 0.5 - int(self.width * 0.004) * 2) * progressBarPercent, self.height * 0.035 - int(self.width * 0.004) * 2))
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
                        self.CLOCK.tick(self.monitorRefreshRate)

            # self.FONT.render_to(self.SCREEN, (self.width*0.4125, self.height*0.25), "Terminal Powering On", (self.pygameColorCodes.get("Light Gray")))
            # pygame.draw.rect(self.SCREEN, (255, 0, 0), (self.width * 0.525, 0, 2, self.height))
            # 0.525 - 0.35 = 0.175 / 23 = 0.00760869565; Each char needs 0.0076 width
            pygame.display.update()

        else:
            pass

    def getDisplayData(self):
        return self.displayData
