import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()
width, height = 800, 600
row = 25 # Length of row and column
dist = 25
cols, rows = width // row, height // row
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game!")
clock = pygame.time.Clock()

class Cube(object):
	def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color
	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
	def draw(self, win, eyes=False):
		i, j = self.pos[0], self.pos[1]
		pygame.draw.rect(win, self.color, (i*dist+1, j*dist+1, dist-2, dist-2))
		if eyes:
			center = dist//2
			radius = 3
			middle_circle1 = (i*dist+center-radius,j*dist+8)
			middle_circle2 = (i*dist+dist-radius*2,j*dist+8)
			pygame.draw.circle(win, (0,0,0), middle_circle1, radius)
			pygame.draw.circle(win, (0,0,0), middle_circle2, radius)

class Snake(object):
	body = []
	turns = {}
	# position is given as coordinates on the grid ex (3, 4)
	def __init__(self, color, pos):
		self.color = color
		self.head = Cube(pos)
		self.body.append(self.head)
		self.dirnx = 0
		self.dirny = 1
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				self.dirnx, self.dirny = -1, 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
			elif keys[pygame.K_UP]:
				self.dirnx, self.dirny = 0, -1
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
			elif keys[pygame.K_RIGHT]:
				self.dirnx, self.dirny = 1, 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
			elif keys[pygame.K_DOWN]:
				self.dirnx, self.dirny = 0, 1
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
		for i, cube in enumerate(self.body):
			pos = cube.pos[:]
			if pos in self.turns:
				turn = self.turns[pos]
				cube.move(turn[0], turn[1])
				if i == len(self.body) -1:
					self.turns.pop(pos)
			else: cube.move(cube.dirnx, cube.dirny)
	def reset(self, pos):
		self.head = Cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1
	def add_cube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny
		if dx == 1 and dy == 0:    self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
		elif dx == -1 and dy == 0: self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
		elif dx == 0 and dy == 1:  self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
		elif dx == 0 and dy == -1: self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))
		self.body[-1].dirnx = dx
		self.body[-1].dirny = dy
	def draw(self, win):
		for i, cube in enumerate(self.body):
			if i == 0: cube.draw(win, True)
			else: cube.draw(win)

def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try: root.destroy()
	except: pass

def redraw_window():
	win.fill((1, 1, 1))
	snake.draw(win)
	snack.draw(win)
	pygame.display.update()

def random_snack(item):
	while True:
		x = random.randrange(1, cols-1)
		y = random.randrange(1, rows-1)
		if len(list(filter(lambda i: i.pos == (x,y), item.body))) > 0: continue
		else: break
	return (x,y)

snake = Snake((255, 0, 0), (10, 10))
snake.add_cube()
snack = Cube(random_snack(snake), color=(0, 255, 0))
run = True
while run:
	pygame.time.delay(50)
	clock.tick(10)
	snake.move()
	if snake.head.pos[0] >= cols or snake.head.pos[0] < 0 or snake.head.pos[1] >= rows or snake.head.pos[1] < 0:
			print("Score:", len(snake.body))
			snake.reset((cols//2, height//row//2))
	if snake.body[0].pos == snack.pos:
		snake.add_cube()
		snack = Cube(random_snack(snake), color=(0, 255, 0))
	for x in range(len(snake.body)):
		if snake.body[x].pos in list(map(lambda i:i.pos, snake.body[x+1:])):
			print("Score:", len(snake.body))
			message_box("Loser!", "C'mon Play again!")
			snake.reset((cols//2, height//row//2))
			break
	redraw_window()
