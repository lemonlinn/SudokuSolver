
#libs
import pandas as pd
import numpy as np
import pygame
import pygame.freetype
import copy
import math
import os
#from solver_techwithtim import *
from Lemon_SudokuSolver import *

th = 450
tw = 390

#constants
pygame.init()
pygame.freetype.init()
screen = pygame.display.set_mode((th,tw))
pygame.display.set_caption('Sudoku Solver')
font = pygame.freetype.Font(None, 22)
otherfont = pygame.font.SysFont(None,22)
text = ''
done = False
#bg = pygame.image.load("grid.jpg")

x = 19
y = 19
h = 35
w = 35
v = 39
e = 354
color = (255,255,255)

zmatrix = np.array([np.zeros(9, np.int)]*9)
blit_list = []

cursor_img = pygame.Surface((h,w), pygame.SRCALPHA)
white_rim = pygame.Surface((h,w), pygame.SRCALPHA)
pygame.draw.rect(white_rim, (255,255,255), white_rim.get_rect(), 11)
pygame.draw.rect(cursor_img, (255,0,0,50), cursor_img.get_rect(), 10)

screen.fill(color)

#functions
def button(msg,x,y,w,h,ic,ac,grid,screen):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	#print(click)
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(screen, color,(x,y,w,h))

		if click[0] == 1:
			#if(valid_input(grid)):
			if(solve_sudoku(grid)):  
				for j,a in enumerate(np.arange(29, 364, 39)):
					for i,b in enumerate(np.arange(29, 364, 39)):
						font.render_to(screen, (a,b), str(grid[i][j]), 
							bgcolor = color, fgcolor = (0,0,0), size = 22)
			else:
				errmsg = otherfont.render("Invalid Input", True, ac)
				font.render_to(screen, (((370-16-errmsg.get_width())//2), ((370-16-errmsg.get_height())//2)), 
					"Invalid Input", bgcolor = ic, fgcolor = (0,0,0), size = 22)
	else:
		pygame.draw.rect(screen, ic,(x,y,w,h))

	#"solve" button
	smallText = pygame.font.SysFont(None, 22)
	#textSurf, textRect = text_objects(msg, smallText)
	textSurf = smallText.render(msg, True, ac)
	textRect = textSurf.get_rect()
	textRect.center = (math.floor(x+(w/2)), math.floor(y+(h/2)) )
	screen.blit(textSurf, textRect)

def gridlines():
	lines_list = [16,55,94,174,213,293,333,370]
	for l in lines_list:
		pygame.draw.aaline(screen, (0, 0, 0), (l, 16), (l, 370))
		pygame.draw.aaline(screen, (0, 0, 0), (16, l), (370, l))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(134, 16, 5, 354))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(251, 16, 5, 354))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(16, 134, 354, 5))
		pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(16, 251, 354, 5))

# sprite stuff

class LoadScreen(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		files = os.listdir("./loading_screen/")
		self.image = [pygame.image.load("./loading_screen/" + name) for name in files]
		self.rect = self.image[0].get_rect()
		self.rect.center = (tw//2,th//2)

		#self.Surface = pygame.Surface([tw,th])

	#def update(self):


#all_sprites = pygame.sprite.Group()
#load = LoadScreen()
#all_sprites.add(load)

files = os.listdir("./loading_screen/")
image = [pygame.image.load("./loading_screen/" + name) for name in files]
image_rect = image[0].get_rect()

#main loop
while not done:
	pygame.time.delay(100)
	pressed = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				# BOOKMARK 5-29-2020: Trying to solve after hitting return
				print(text)
				print(zmatrix)
				#screen.blit(load, (load.rect.center[0], load.rect.center[1]))
				for img in image:				
					screen.blit(img, (tw//2,th//2))
				if(valid_input(zmatrix)):
					if(solve_sudoku(zmatrix)):  
						for j,a in enumerate(np.arange(29, 364, 39)):
							for i,b in enumerate(np.arange(29, 364, 39)):
								font.render_to(screen, (a,b), str(zmatrix[i][j]), 
									bgcolor = color, fgcolor = (0,0,0), size = 22)
				else:
					errmsg = otherfont.render("Invalid Input", True, (0,0,0))
					font.render_to(screen, (((370-16-errmsg.get_width())//2), ((370-16-errmsg.get_height())//2)), 
					"Invalid Input", bgcolor = (255,125,125), fgcolor = (0,0,0), size = 22)

				print(zmatrix)
			#elif event.key == pygame.K_BACKSPACE:
				#text = ""
				#pygame.draw.rect(screen, color, pygame.Rect(x,y,h,w))
			elif event.key == pygame.K_DELETE:
				text = ''
				zmatrix = np.array([np.zeros(9, np.int)]*9)
				screen.fill(color)
			elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, 
			pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
				text += event.unicode
			elif event.key == pygame.K_0:
				pygame.draw.rect(screen, color, pygame.Rect(x,y,h,w))
				text = event.unicode

	#grid traversal
	if pressed[pygame.K_LEFT] and x > v:
		screen.blit(white_rim, (x,y))
		x -= v
		text = ''
		screen.blit(white_rim, (x,y))
		screen.blit(cursor_img, (x,y))
	elif pressed[pygame.K_RIGHT] and x < (e-v):
		screen.blit(white_rim, (x,y))
		x += v
		text = ''
		screen.blit(white_rim, (x,y))
		screen.blit(cursor_img, (x,y))
	elif pressed[pygame.K_DOWN] and y < (e-v):
		screen.blit(white_rim, (x,y))
		y += v
		text = ''
		screen.blit(white_rim, (x,y))
		screen.blit(cursor_img, (x,y))
	elif pressed[pygame.K_UP] and y > v:
		screen.blit(white_rim, (x,y))
		y -= v
		text = ''
		screen.blit(white_rim, (x,y))
		screen.blit(cursor_img, (x,y))

	else:
		screen.blit(white_rim, (x,y))
		screen.blit(cursor_img, (x,y))

	#draw grid
	gridlines()

	button("Solve", 380, math.floor(390/2), 60, 30, (255,125,125), (0,0,0), zmatrix, screen)

	#display numbers/write numbers to matrix
	for j,a in enumerate(np.arange(19,e,v)):
		for i,b in enumerate(np.arange(19,e,v)):
			if x == a and y == b:
				if len(text) == 1 and text != "0":
					zmatrix[i][j] = int(text)
					#screen.blit(bg, (15,15))
					blit_list.append(copy.deepcopy(font.render_to(screen, (a+10,b+10), text, bgcolor = color, fgcolor = (0,0,0), size = 22)))
					for val in blit_list:
						val
				elif len(text) == 0 or text == "0":
					zmatrix[i][j] == 0

	#end of main loop
	pygame.display.flip()



#graveyard
#for a in np.arange(15,350,125):
		#for b in np.arange(15,350,125):
			#for c in np.arange(a, (a+120), 40):
				#for d in np.arange(b, (b+120), 40):
					#if event.type == pygame.MOUSEBUTTONDOWN:
						#if event.button == 1:
							#color = (255,0,0)
						#elif event.button == 3:
							#color = (255,255,255)
					#pygame.draw.rect(screen, color, pygame.Rect(c,d,35,35))