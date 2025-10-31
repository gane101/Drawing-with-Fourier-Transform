import pygame
import pandas as pd

pygame.init()

screen = pygame.display.set_mode((800,500))
done = False

xpoints = []
ypoints = []
recording = False

t = 0
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		# print(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			recording = True
		elif event.type == pygame.MOUSEBUTTONUP:

			i=0
			while i < len(xpoints)-1:
				if xpoints[i] == xpoints[i+1] and ypoints[i] == ypoints[i+1]:
					del xpoints[i+1]
					del ypoints[i+1]
					i -=1
				i+=1

			data = {
				"x" : xpoints,
				"y" : ypoints
			}

			df = pd.DataFrame(data)

			df.to_csv("Path.csv")

			done = True

	screen.fill((128,128,128))

	if recording:
		t += 1
		if t % 10 == 0:
			xpoints.append(pygame.mouse.get_pos()[0]-400)
			ypoints.append(-pygame.mouse.get_pos()[1]+250)

	for i in range(len(xpoints)):
		pygame.draw.circle(screen, (0,0,0), (xpoints[i]+400,250-ypoints[i]), 2)

	pygame.display.flip()

