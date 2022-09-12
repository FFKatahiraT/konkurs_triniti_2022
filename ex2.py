import pygame
import numpy as np

def particle_force(force_multiplier, scale_multiplier):
	#define particle potental E(r) curve
	#E [Ha], r [A]
	eps = 0.0005005018809095022
	sigma = 3.392176105163491
	r_list = [0]
	for i in range(1,1000):	#from 1 because of E0 nullify
		r_list.append(i**2/1e5) 	#1 -- 10 A

	E_list = [0] #first value nullified for avoiding particle interaction with itself
	for x in r_list[1:]:
		E_list.append(4*eps*((sigma/x)**12-(sigma/x)**6))

	for i in range(len(r_list)):	#manage the model scale px -- A
		r_list[i] *= scale_multiplier

	#define particle interaction force F=dE/dr
	F_list = [0]
	for i in range(len(E_list)-1):
		F_list.append((E_list[i+1]-E_list[i])/(r_list[i+1]-r_list[i])*force_multiplier) #[Ha/A]
	# for i in range(len(F_list[:300])):
	# 	F_list[i] = -1*force_multiplier
		
	return r_list, E_list, F_list
	
class particle_class():
	def __init__(self, pos_x, pos_y, x_speed, mass, color):
		self.size = 5
		self.color = color
		self.m = mass
		self.x_speed = x_speed
		self.y_speed = 0
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.past_pos_x = []
		self.past_pos_y = []

	def position_upd(self):
		#Calc forces, affecting on a particle
		#returns speeds
		self.Fx_summ, self.Fy_summ = 0, 0
		for particle in particles_list:
			#Calc force superposition
			Fx_temp, Fy_temp = find_F(self.pos_x, self.pos_y, particle.pos_x, particle.pos_y)
			self.Fx_summ += Fx_temp
			self.Fy_summ += Fy_temp
		
		self.x_speed += self.Fx_summ/self.m	#[Ha/A/amu]
		self.y_speed += self.Fy_summ/self.m

		# self.x_speed /= 1+1e-3	
		# self.y_speed /= 1+1e-3		

	def out_of_borders(self):
		global particle_exist
		if self.pos_x > display_width:
			# print('self.pos_x > display_width:')
			# self.pos_x = self.size//2
			particle_exist = False
			# self.x_speed *= -1
			# self.pos_x = display_width - self.size//2
		elif self.pos_x < 0:
			# print('self.pos_x < 0:')
			# self.pos_x = display_width - self.size//2
			particle_exist = False
			# self.x_speed *= -1
			# self.pos_x = self.size//2
		elif self.pos_y > display_height:
			# print('self.pos_y')
			# self.pos_y = self.size//2
			particle_exist = False
			# self.y_speed *= -1
			# self.pos_y = display_height - self.size//2
		elif self.pos_y < 0:
			# print('self.pos_y < 0:', self.pos_y)
			# self.pos_y = display_height - self.size//2
			particle_exist = False
			# self.y_speed *= -1
			# self.pos_y = self.size//2

	def update(self):
		#update particle position
		#[Ha/A/amu]*time time[1/FPS]
		#[Ha/(A*amu*FPS)] to [J*s/(m*kg)]
		#Ha=4.36*10**-18 J, A=10**-10 m, amu=1.67*10**-27 kg, FPS = 1/60 s
		#[Ha/(A*amu*FPS)] = 1.566467065868264e+21 [J*s/(m*kg)] = [m]
		#need multiply pos by: 1.566467065868264e+21/time_multiplier to get [m] dimension
		self.position_upd()
		self.pos_x += self.x_speed*time_multiplier
		self.pos_y += self.y_speed*time_multiplier
		self.past_pos_x.append(self.pos_x)
		self.past_pos_y.append(self.pos_y)
		self.out_of_borders()	#check if particle out of border
		# pygame.draw.circle(gameDisplay, self.color, (int(self.pos_x),int(self.pos_y)), int((self.Fx_summ**2+self.Fy_summ**2)**0.5))
		pygame.draw.circle(gameDisplay, self.color, (int(self.pos_x),int(self.pos_y)), self.size)

def find_F(pos_x, pos_y, opponent_pos_x, opponent_pos_y):
	# finds F related to the nearest position r_list
	delta_x = abs(pos_x - opponent_pos_x)
	delta_y = abs(pos_y - opponent_pos_y)
	r = (delta_x**2+delta_y**2)**0.5
	delta, delta_prev = 0, -1
	# if abs(r - r_list[i]) == 0:	#If delta = 0 --> Force = 0
	# 	F = 0
	for i in range(len(r_list)):	#find index of the nearest force value
		if r <= r_list[i]:
			break
		# print(delta, 'delta')
		# print(r_list[i], 'r_list')
	F = F_list[i-1]
	# print(F, 'F')
	
	if delta_x!=0: 
		Fx = F/(1+delta_y**2/delta_x**2)**0.5 
	else: 
		Fx=0
	Fy = (F**2-Fx**2)**0.5
	#axis projection added
	#absolute -F - repulsion, +F - attraction
	# print(F, particles_list[0].pos_x - particles_list[-1].pos_x)
	if F > 0:
		if pos_x > opponent_pos_x:
			Fx *= -1
		if pos_y > opponent_pos_y: 
			Fy *= -1
	elif F < 0:
		if pos_x > opponent_pos_x:
			Fx *= -1
		if pos_y < opponent_pos_y:
			Fy *= -1
	return Fx, Fy


def blit():
	#Displaying elements
	gameDisplay.fill(bg_color)
	for particle in particles_list:
		particle.update()

def calc_sinTheta():
	#Calcs sin theta only
	global theta_rad_list
	delta_x = abs(particles_list[1].past_pos_x[-4] - particles_list[1].pos_x)
	# delta_x = abs(particles_list[0].pos_x - particles_list[1].pos_x)
	delta_y = abs(particles_list[1].past_pos_y[-4] - particles_list[1].pos_y)
	# delta_y = abs(particles_list[0].pos_y - particles_list[1].pos_y)
	sinTheta = delta_y/(delta_x**2+delta_y**2)**0.5
	theta_rad_list.append(np.arcsin(sinTheta))
	return sinTheta

def calc_cross_section(sinTheta):
	#Calcs dTheta & sigma list
	global sigma_list
	dTheta = abs(theta_rad_list[-1] - theta_rad_list[-2])
	sigma_list.append(b_list[exp_num]*db/(sinTheta*dTheta))
	# particle_speed = (particles_list[1].x_speed**2 + particles_list[1].y_speed**2)**0.5
	# E_k = particles_list[1].m*particle_speed**2/2
	# sigma_list.append((1/(4*E_k))**2/np.sin(theta_rad_list[-1]/4)**4)	#Dimension: 1/[speed_sqr*aem]**2*e**2

def generate_particle():
	global particles_list
	particles_list.append(particle_class(200, display_width//2-b_list[exp_num],4, 40, particle_color[1]))

if __name__ == '__main__':
	###############PARAMETERS & INITIALIZING###############
	pygame.init()
	pygame.font.init()
	myfont = pygame.font.SysFont('Comic Sans MS', 36)

	display_width, display_height = 800, 600
	display_size = (display_width, display_height)
	gameDisplay = pygame.display.set_mode(display_size)

	pygame.display.set_caption('MD')
	clock = pygame.time.Clock()

	scale_multiplier = 100
	force_multiplier = 1
	time_multiplier = 1	#affects on time only. DOESN'T WORK
	white = (255,255,255)
	black = (0,0,0)
	gray = (125,125,125)
	blue = (0,0,255)
	light_blue = (130,130,255)
	red = (255,0,0)
	rose = (255,130,130)
	FPS = 60
	dark_theme = True
	if dark_theme:
		particle_color, bg_color = (rose, light_blue), black
	else:
		particle_color, bg_color = (red, blue), white

	particles_list = []	#generate particles
	b_list, theta_rad_list, sigma_list = [], [], []
	exp_num = 0
	exp_max_num = 200
	db = 1
	for i in range(exp_max_num): b_list.append(i*db)	#impact parameter
	for i in range(exp_max_num//2):
		b_list[i], b_list[-(i+1)] = b_list[-(i+1)], b_list[i]
	file = open('ex2.dat', 'w')
	file.write('% b, sigma, Theta \n')
	print('b', 'sigma', 'Theta')
	# print('F', 'x')	
	particle_exist = True
	running = True
	
	r_list, E_list, F_list = particle_force(force_multiplier, scale_multiplier) #Calc particle potential
	particles_list.append(particle_class(500, display_width//2, 0,4e12, particle_color[0])) #generate target particle
	generate_particle()
	############################################################
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running=False
		if not particle_exist and exp_num >= exp_max_num - 1:
			running = False
		elif not particle_exist:	#generate new particle, if old ones gone
			sinTheta = calc_sinTheta()
			if exp_num >= 1:
				calc_cross_section(sinTheta)
				text = (str(b_list[exp_num])+','
					+str(sigma_list[exp_num-1])+','
					+str(theta_rad_list[exp_num-1]*180/np.pi)+'\n')
				file.write(text)
				print(text, end='')
			del particles_list[-1:]
			generate_particle()
			particle_exist = True
			exp_num += 1
		blit()
		pygame.display.update()
		clock.tick(FPS)
	else:
		sigma_summ = 0
		for i in range(1, len(sigma_list)):	#theta from 0 to pi is needed
			sigma_summ += sigma_list[i]*(theta_rad_list[i]-theta_rad_list[i-1])/np.pi
		#DIMENSION
		#[Ha/A/amu]
		#Ha=4.36*10**-18 J, A=10**-10 m, amu=1.67*10**-27 kg
		# Ha, A, amu = 4.36*10**-18, 10**-10*scale_multiplier, 1.66*10**-27
		#need multiply speed by: [Ha/(A*amu)] = --//-- [J*s/(m*kg)] => to get [m/s] dimension
		#E_k = particles_list[1].m*particle_speed**2/2: amu*2.610778443113773e+19**2 = --//-- [J]
		# E_dimension_multiplier = (Ha/A)**2/amu #should be Ha dim
		#e**4/(E_k)**2, sigma : 
		# e = 1.60217663 * 10**-19
		sigma_summ *= 2	#because we integrated from 0 to 180 deg. Just multiplied by 2 because of symmetry
		sigma_summ /= scale_multiplier**2	#recover original scale [A]
		print(sigma_summ, 'sigma_summ [A^2]')	#if sigma ~3.4 A --> sigma should be around 10 A^2
		file.write(str(sigma_summ)+' integral cross section [A^2]')
		file.close()