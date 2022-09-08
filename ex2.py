import pygame

def particle_force():
	#define particle potental E(r) curve
	#E [Ha], r [A]
	eps = 0.0005005018809095022
	sigma = 3.392176105163491
	r_list = [0]
	for i in range(1,1000):	#from 1 because of E0 nullify
		r_list.append(i/1e2) 	#1 -- 10 A

	E_list = [0] #first value nullified for avoiding particle interaction with itself
	for x in r_list[1:]:
		E_list.append(4*eps*((sigma/x)**12-(sigma/x)**6))


	#define particle interaction force F=dE/dr
	F_list = [0]
	for i in range(len(E_list)-1):
		F_list.append((E_list[i+1]-E_list[i])/(r_list[i+1]-r_list[i])) #[Ha/A]
	for i in range(len(r_list)):	#manage the model scale px -- A
		r_list[i] *= scale_multiplier
	return r_list, F_list
	
class particle_class():
	def __init__(self, pos_x, pos_y, x_speed, mass, color):
		self.size = 5
		self.color = color
		self.m = mass
		self.x_speed = x_speed
		self.y_speed = 0
		self.pos_x = pos_x
		self.pos_y = pos_y

	def position_upd(self):
		#Calc forces, affecting on a particle
		#returns speeds
		Fx_summ, Fy_summ = 0, 0
		for particle in particles_list:
			#Calc force superposition
			Fx_summ += find_F(self.pos_x, particle.pos_x)
			Fy_summ += find_F(self.pos_y, particle.pos_y)
		
		self.x_speed += Fx_summ/self.m 	#[Ha/A/amu]
		self.y_speed += Fy_summ/self.m

	def out_of_borders(self):
		if self.pos_x > display_width:
			self.x_speed *= -1
			self.pos_x = display_width - self.size//2
		elif self.pos_x < 0:
			self.x_speed *= -1
			self.pos_x = self.size//2
		if self.pos_y > display_height:
			self.y_speed *= -1
			self.pos_y = display_height - self.size//2
		elif self.pos_y < 0:
			self.y_speed *= -1
			self.pos_y = self.size//2

	def update(self):
		#update particle position
		#[Ha/A/amu]*time time[1/FPS]
		#[Ha/(A*amu*FPS)] to [J*s/(m*kg)]
		#Ha=4.36*10**-18 J, A=10**-10 m, amu=1.67*10**-27 kg, FPS = 1/60 s
		#[Ha/(A*amu*FPS)] = 1.566467065868264e+21 [J*s/(m*kg)] = [m]
		#need multiply pos by: 1.566467065868264e+21/multiplier to get [m] dimension
		self.position_upd()
		self.pos_x += self.x_speed*time_multiplier
		self.pos_y += self.y_speed*time_multiplier
		self.out_of_borders()	#check if particle out of border
		pygame.draw.circle(gameDisplay, self.color, (int(self.pos_x),int(self.pos_y)), self.size)

def find_F(pos, opponent_pos):
	# finds F related to the nearest position r_list
	r = abs(pos - opponent_pos)
	i = 0
	delta, delta_prev = 0, 0
	if abs(r - r_list[i]) == 0:	#If delta = 0 --> Force = 0
		F = 0
	else:
		while delta_prev < delta:	#find index of the nearest force value
			delta_prev = delta
			delta = abs(r - r_list[i])
			i += 1
		F = F_list[i-1]
	#axis projection added
	#absolute -F - repulsion, +F - attraction
	if pos > opponent_pos: F*=-1 
	return F


def blit():
	#Displaying elements
	gameDisplay.fill(white)
	for particle in particles_list:
		particle.update()


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 36)

display_width, display_height = 800, 600
display_size = (display_width, display_height)
gameDisplay = pygame.display.set_mode(display_size)

pygame.display.set_caption('MD')
clock = pygame.time.Clock()

scale_multiplier = 10
time_multiplier = 1e3	#affects on time only
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
FPS = 60

r_list, F_list = particle_force() #Calc particle potential

particles_list = []	#generate particles
for i in range(20):
	for j in range(1):
		particles_list.append(particle_class(200+10*j, 200+10*i,0, 40, blue))
particles_list.append(particle_class(500, 300, 0,4e9, red)) #generate target particle

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running=False

	blit()
	pygame.display.update()
	clock.tick(FPS)