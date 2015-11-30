import sys, pygame, math, random

pygame.init()

####
gamespeed = 1000

size = width, height = 800, 640
black = 0, 0, 0
red = 255, 0, 0

pkey = 0
curbug = 0
lock = False

screen = pygame.display.set_mode(size)

blockpos = (0,0)
cursorsize = 2
spsize = 16

bugd = dict()
playd = dict()
addqueue = dict()
dbugd = dict()

cursorsnd = pygame.mixer.Sound("bloop5.wav")
tabsnd = pygame.mixer.Sound("bloop2.wav")
pygame.mixer.music.load("bg.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

pygame.mouse.set_visible(False)

bdiag = pygame.Surface((140,size[1]), flags=pygame.SRCALPHA)
brect = bdiag.get_rect()
brect.move(50,50)

bfont = pygame.font.Font(None, 18)
btext = bfont.render("you are the virus", True, (255,255,255)) 

####

def clearaddq():
	global addqueue
	addqueue = dict()

def addbug(bugpos, bugtype):
	k = newkey()
	addqueue[k] = Bug(bugpos, bugtype, k)

def addplay(playpos, playtype):
	if playtype == 0: playd[newkey()] = Player(playpos, playtype)
	elif playtype == 1: playd[newkey()] = Player(playpos, playtype)
	elif playtype == 2: playd[newkey()] = Player(playpos, playtype)
	elif playtype == 3: playd[newkey()] = Player(playpos, playtype)

def newkey():
	global pkey
	pkey += 1
	return pkey

class Bug:
	def __init__(self, mypos, mytype, key):
		self.framex = 0
		self.framey = 0
		self._delay = 300
		self._last  = 0
		self._delayu = 300
		self._lastu  = 0
		self.key = key
		self.birth = 0
		
		self.setbugtype(mytype)

		self.sur = pygame.transform.scale(self.sur, (self.sur.get_width()*2,self.sur.get_height()*2))
		self.rect = self.sur.get_rect()
		self.sur = self.sur.subsurface(self.rect)
		self.rect = self.rect.move(mypos)
		self.buf = self.sur.copy()
		self.px = mypos[0]
		self.py = mypos[1]
		self.x = mypos[0]/spsize
		self.y = mypos[1]/spsize
		self.adjn = self.checkadj(0)
		self.adje = self.checkadj(1)
		self.adjs = self.checkadj(2)
		self.adjw = self.checkadj(3)

	def checkadj(self, direction):
		if direction == 0:
			x = self.x
			y = self.y-1
		elif direction == 1:
			x = self.x+1
			y = self.y
		elif direction == 2:
			x = self.x
			y = self.y+1
		elif direction == 3:
			x = self.x-1
			y = self.y
		for b in bugd:
			if bugd[b].x == x and bugd[b].y == y: return True
		return False

	def checkdadj(self, direction):
		if direction == 0:
			x = self.x
			y = self.y-1
		elif direction == 1:
			x = self.x+1
			y = self.y
		elif direction == 2:
			x = self.x
			y = self.y+1
		elif direction == 3:
			x = self.x-1
			y = self.y
		for b in dbugd:
			if dbugd[b].x == x and bugd[b].y == y: return True if bool(random.randint(0,1)) else False
		return False
	
	def setbugtype(self, mytype):
		if mytype == 0:
			self.sur = pygame.image.load("E.png")
			self.hp = 100
			self.growf = 2
			self.ttl = 520000
		if mytype == 1:
			self.sur = pygame.image.load("F.png")
			self.hp = 45
			self.growf = 4
			self.ttl = 400000
		if mytype == 2:
			self.sur = pygame.image.load("G.png")
			self.hp = 10
			self.growf = 5
			self.ttl = 220000
		if mytype == 3:
			self.sur = pygame.image.load("H.png")
			self.hp = 2
			self.growf = 11
			self.ttl = 99000
		self.bugtype = mytype

	def draw(self):
		self.doanim(pygame.time.get_ticks())
		self.doblit(self.sur)
		return self.update(pygame.time.get_ticks())

	def doblit(self, surf):
		screen.blit(surf, self.rect, (0,0,spsize,spsize))
		

	def doanim(self, t):
		if t - self._last > self._delay:
			if self.framex<3:
				self.sur.scroll(-spsize,0)
				self.framex+=1
			else:
				self.sur = self.buf.copy()
				self.framex = 0
			self._last = t

	def update(self, t):
		global gamespeed
		if t - self._lastu > self._delayu:
			self.hp -= float(gamespeed)/float(self.ttl)
			if self.hp <= 0: return False
			self.adjn = self.checkadj(0)
			self.adje = self.checkadj(1)
			self.adjs = self.checkadj(2)
			self.adjw = self.checkadj(3)
			if self.birth >= gamespeed:
				r = random.randint(0,3)
				if r == 0:
					if not self.adjn:
						addbug((self.px,self.py-16), self.bugtype)
				elif r == 1:
					if not self.adje:
						addbug((self.px+16,self.py), self.bugtype)
				elif r == 2:
					if not self.adjs:
						addbug((self.px,self.py+16), self.bugtype)
				elif r == 3:
					if not self.adjw:
						addbug((self.px-16,self.py), self.bugtype)
				self.birth = 0
			self._lastu = t
			self.birth += self.growf
		return True
				
		

class Player:
	def __init__(self, mypos, mytype):
		return True

####
stufft = 0
stuffl = 0
stuffc = 6.28
stuffs = pygame.Surface(size, flags=pygame.SRCALPHA)
stuffs.fill((0,0,0,0))

def docoolstuff(surf):
	global stufft, stuffc, stuffl
	t = pygame.time.get_ticks()
	d1 = 10
	d2 = 2000
	d3 = 6000
	if stufft > d1:
		for b in bugd:
			if bugd[b].bugtype == 0: pygame.draw.arc(surf, (math.sin(t/d2) % 255, 128, 0), (bugd[b].px-248, bugd[b].py-120, 256, 256), 0, stuffc)
			elif bugd[b].bugtype == 1: pygame.draw.arc(surf, (math.sin(t/d3) % 255, 25, 0), (bugd[b].px-120, bugd[b].py+8, 256, 256), math.pi*.5, stuffc+math.pi*.5)
			elif bugd[b].bugtype == 2: pygame.draw.arc(surf, (55, math.sin(t/d2)%255, 0), (bugd[b].px+8, bugd[b].py-120, 256, 256), math.pi, stuffc+math.pi)
			elif bugd[b].bugtype == 3: pygame.draw.arc(surf, (55, math.sin(t/d3)%255, 180), (bugd[b].px-120, bugd[b].py-248, 256, 256), math.pi*1.5, stuffc+math.pi*1.5)
		stuffc += 0.0001
		if stuffc > 2*math.pi: stuffc = 0
		stufft = 0
	stufft += t - stuffl
	stuffl = t

def switchbug():
	global curbug, bdiag, btext
	curbug = (curbug+1 if curbug < 3 else 0)
	btext = bfont.render("Activate unit 00" + str(curbug), True, (255,255,255)) 

####

while 1:
	for event in pygame.event.get():
        	if event.type == pygame.QUIT: sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			cursorsize = 4
			cursorsnd.play()
			addbug(blockpos, curbug)
		elif event.type == pygame.MOUSEBUTTONUP:
			cursorsize = 2
		elif event.type == pygame.KEYDOWN:
			if pygame.key.get_pressed()[pygame.K_TAB]:
				tabsnd.play()
				switchbug()

	pos = pygame.mouse.get_pos()
	blockpos = (pos[0]-pos[0]%spsize,pos[1]-pos[1]%spsize)

	screen.fill(black)
	docoolstuff(stuffs)
	screen.blit(stuffs,(0,0))

	pygame.draw.rect(screen, red, pygame.Rect(blockpos, (spsize,spsize)), cursorsize)

	####
	killd = dict()
	lock = True
	for x in bugd:
		if bugd[x].draw() == False:
			killd[newkey()] = x
			dbugd[newkey()] = (bugd[x].x,bugd[x].y)
	lock = False

	for x in killd:
		print "killing bug" + str(killd[x])
		if not lock: del bugd[int(killd[x])]

	for x in addqueue:
		print "adding bug" + str(x)
		if not lock: bugd[x] = addqueue[x]
	clearaddq()

	bdiag.fill((0,0,0,0))
	bdiag.blit(btext,brect)
	screen.blit(bdiag, bdiag.get_rect())

	####

	pygame.display.flip()
