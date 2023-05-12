# Import
import pygame
import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import time

# Initialize
pygame.init()

# Creat Window /Display
width, height =  600, 400
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Balloon Popper")

# Initial Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1200) # width
cap.set(4, 1000) # height

# Images
imgBalloon = pygame.image.load('images/balloon.png').convert_alpha()
rectBalloon = imgBalloon.get_rect()
rectBalloon.x,rectBalloon.y = 400, 200

# Variables
speed = 5
score = 0
scoreb = 0
startTime = time.time()
totalTime = 100

# Detector
detector = HandDetector(detectionCon=0.4, maxHands=1)

def resetBalloon():
	rectBalloon.x = random.randint(100, img.shape[1] - 100)
	rectBalloon.y = img.shape[0] + 50

# Main Loop
start = True
while start:
	# Get events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			start = False
			pygame.quit()

	# Apply Logic
	# window.fill((0, 255, 0))
	timeRemain = int(totalTime - (time.time()-startTime))

	if timeRemain < 0:
		# window.fill((0, 67, 25))
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		imgRGB = np.rot90(imgRGB)
		frame = pygame.surfarray.make_surface(imgRGB).convert()
		frame = pygame.transform.flip(frame, True, False)
		window.blit(frame, (0, 0))

		font = pygame.font.Font(None, 50)
		textScore = font.render(f'Your Score: {score}', True, (255, 50, 50))
		textScoreb = font.render(f'Total Crash: {scoreb}', True, (255, 50, 50))
		textTime = font.render(f'Time Up', True, (255, 50, 50))
		window.blit(textScore, (450,400))
		window.blit(textScoreb, (450,350))
		window.blit(textTime, (490,300))

	else:
		# OpenCv
		success, img = cap.read()
		img = cv2.flip(img, 1)

		hands = detector.findHands(img, flipType=False )  # without draw
		# hands, img = detector.findHands(img, flipType=False) # with draw

		rectBalloon.y -= speed # Move ballon Up
		# Check if Ballon hs reached the top without pop
		if rectBalloon.y <0:
			resetBalloon()
			speed += 1


		if hands:
			hand = hands[0]
			#print (hand)
			x, y  = hand[0]['lmList'][8][:2]

			if rectBalloon.collidepoint(x, y):
				resetBalloon()
				score += 5
				speed += 1
				scoreb += 1


		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		imgRGB = np.rot90(imgRGB)
		frame = pygame.surfarray.make_surface(imgRGB).convert()
		frame = pygame.transform.flip(frame, True, False)
		window.blit(frame, (0, 0))
		window.blit(imgBalloon, (rectBalloon))

		font = pygame.font.Font(None, 50)
		textScore = font.render(f'Total Score: {score}', True, (255, 50, 50))
		textScoreb = font.render(f'Total Crash: {scoreb}', True, (255, 50, 50))
		textTime = font.render(f'Remaing Time: {timeRemain}', True, (255, 50, 50))
		window.blit(textScore, (35,35))
		window.blit(textScoreb, (35,80))
		window.blit(textTime, (915,35))

	# Upate Display
	pygame.display.update()

	# Set FPS
	clock.tick(fps)