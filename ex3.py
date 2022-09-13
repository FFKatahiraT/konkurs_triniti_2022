import pygame
import numpy as np
import random

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
	def __init__(self, pos_x, pos_y, x_speed, y_speed, mass, color):
		self.size = 5
		self.color = color
		self.m = mass
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.delta_pos_x = 0
		self.delta_pos_y = 0
		self.sign_x_speed = 0	#-1: negative, 1: positive, 0: idle
		self.sign_y_speed = 0
		self.impact_pos_x = 0
		self.impact_pos_y = 0
		self.impact_speed_summ = 0	#Determine speed after impact

	def position_upd(self):
		#Calc forces, affecting on a particle
		#returns speeds
		#Taking into account particles out of the borders
		width_shift, height_shift = [0], [0]
		if self.pos_x > display_width*0.8:
			width_shift.append(1)	
		elif self.pos_x < display_width*0.2:
			width_shift.append(-1)
		if self.pos_y > display_height*0.8:
			height_shift.append(1)	
		elif self.pos_y < display_height*0.2:
			height_shift.append(-1)

		self.Fx_summ, self.Fy_summ = 0, 0
		for w_shift in width_shift:
			for h_shift in height_shift:
				for particle in particles_list:
					#Calc force superposition
					Fx_temp, Fy_temp = find_F(self.pos_x, self.pos_y, 
						self.delta_pos_x, self.delta_pos_y,
						particle.pos_x+display_width*w_shift, 
						particle.pos_y+display_height*h_shift)
					self.Fx_summ += Fx_temp
					self.Fy_summ += Fy_temp
		
		#F0 = self.Fx_summ & self.Fy_summ
		a_x = self.Fx_summ/self.m
		a_y = self.Fy_summ/self.m
		self.x_speed += a_x*dt
		self.y_speed += a_y*dt
		new_pos_x = self.pos_x + self.x_speed*dt + a_x*dt**2/2
		new_pos_y = self.pos_y + self.y_speed*dt + a_y*dt**2/2
		self.delta_pos_x = abs(new_pos_x - self.pos_x)
		self.delta_pos_y = abs(new_pos_y - self.pos_y)
		self.pos_x = new_pos_x
		self.pos_y = new_pos_y
		
		# self.x_speed += self.Fx_summ/self.m	#[Ha/A/amu]
		# self.y_speed += self.Fy_summ/self.m

	def impact(self):
		global free_path_list
		#add free path after detected impact
		free_path_list.append(((self.pos_x-self.impact_pos_x)**2+(self.pos_y-self.impact_pos_y)**2)**0.5)
		self.impact_pos_x = self.pos_x
		self.impact_pos_y = self.pos_y
		self.impact_speed_summ += (self.x_speed**2+self.y_speed**2)**0.5

	def check_for_impact(self):
		#Detect collisions to determine free path
		if self.x_speed > 0 and self.sign_x_speed != 1:
			self.sign_x_speed = 1
			self.impact()
		elif self.x_speed < 0 and self.sign_x_speed != -1:
			self.sign_x_speed = -1
			self.impact()
		if self.y_speed > 0 and self.sign_y_speed != 1:
			self.sign_y_speed = 1
			self.impact()
		elif self.y_speed < 0 and self.sign_y_speed != -1:
			self.sign_y_speed = -1
			self.impact()
		pass

	def out_of_borders(self):
		if self.pos_x > display_width:
			# print('self.pos_x > display_width:')
			self.pos_x = 0
			# self.x_speed *= -1
			# self.pos_x = display_width - self.size//2
		elif self.pos_x < 0:
			# print('self.pos_x < 0:')
			self.pos_x = display_width - 0
			# self.x_speed *= -1
			# self.pos_x = self.size//2
		elif self.pos_y > display_height:
			# print('self.pos_y')
			self.pos_y = 0
			# self.y_speed *= -1
			# self.pos_y = display_height - self.size//2
		elif self.pos_y < 0:
			# print('self.pos_y < 0:', self.pos_y)
			self.pos_y = display_height - 0
			# self.y_speed *= -1
			# self.pos_y = self.size//2

	def update(self):
		#update particle position
		self.position_upd()
		self.check_for_impact()
		self.out_of_borders()	#check if particle out of border
		pygame.draw.circle(gameDisplay, self.color, (int(self.pos_x),int(self.pos_y)), self.size)

def find_F(pos_x, pos_y, delta_pos_x, delta_pos_y, opponent_pos_x, opponent_pos_y):
	# finds F related to the nearest position r_list
	delta_x = abs(pos_x - opponent_pos_x)
	delta_y = abs(pos_y - opponent_pos_y)
	r = (delta_x**2+delta_y**2)**0.5
	r_delta = (delta_pos_x**2+delta_pos_y**2)**0.5
	delta, delta_prev = 0, -1
	for i in range(len(r_list)):	#find index of the nearest force value
		if r <= r_list[i]:
			break
	if r!=0:
		F = F_list[i-1]*r_delta/r
	else:
		F = 0
	
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

def calc_free_path():
	global free_path_list
	free_path = 0
	free_path_list = free_path_list[Nparticles_in_column*Nparticles_in_row*2:]
	for lmb in free_path_list:
		free_path += lmb
	free_path /= len(free_path_list)
	return free_path/scale_multiplier

def calc_av_speed():
	particle_av_speed = 0
	for particle in particles_list:
		particle_av_speed += particle.impact_speed_summ/len(free_path_list)	#calc sum of average speed of particles
	average_velocity = particle_av_speed/(Nparticles_in_column*Nparticles_in_row)	#calc average velocity
	return average_velocity/scale_multiplier

def blit():
	#Displaying elements
	gameDisplay.fill(bg_color)
	for particle in particles_list:
		particle.update()

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

	scale_multiplier = 1
	force_multiplier = 1
	time_multiplier = 0.2*10**-10	#affects on time only.
	white = (255,255,255)
	black = (0,0,0)
	gray = (125,125,125)
	blue = (0,0,255)
	light_blue = (130,130,255)
	red = (255,0,0)
	rose = (255,130,130)
	FPS = 60
	dt = 1/FPS
	dark_theme = True
	if dark_theme:
		particle_color, bg_color = white, black
	else:
		particle_color, bg_color = blue, white

	particles_list = []	#generate particles
	running = True
	
	free_path_list = []

	r_list, E_list, F_list = particle_force(force_multiplier, scale_multiplier) #Calc particle potential
	Nparticles_in_row = 3	#for p=1 bar ~11.6 particles needed for 800x600 px area (1 px = 1 A if scale_multiplier=1)
	Nparticles_in_column = 4
	init_speed = 13.67*10**10*time_multiplier*scale_multiplier*6
	mass = 40
	for i in range(Nparticles_in_row):
		for j in range(Nparticles_in_column):
			init_speed_x = random.randint(0, int(init_speed*100))/100
			sign_bool = random.choice([-1, 1])
			particles_list.append(particle_class(50+(display_width-50)/Nparticles_in_row*i, 
			50+(display_height-50)/Nparticles_in_column*j, 
			init_speed_x*sign_bool, (init_speed**2-init_speed_x**2)**0.5*sign_bool,
			mass, particle_color)) #generate target particle
	############################################################
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running=False
		
		if len(free_path_list) > 25+Nparticles_in_column*Nparticles_in_row*2:
			running = False
		blit()
		pygame.display.update()
		clock.tick(FPS)
	else:
		#if T=300K average velocity should be 13.67 m/s, 
		#so time moving 10^10 times slower, then velocity would be 13.67 px/s
		k = 1.38*10**-23
		T = 300
		R = 8.31
		cp = 3/2*R
		cv = cp/mass
		c = (3*k*T/mass)**0.5
		sigma = 10.29*10**-20	#From ex2 [m^2]
		N_total = Nparticles_in_column*Nparticles_in_row
		Volume = display_width*display_height*10**-30*scale_multiplier**2
		density = N_total*mass*1.66054e-27/Volume	#amu/A^2 --> *1.66054e-27/10**-30 kg/m^3, should be 1.78 kg/m^3
		free_path = calc_free_path()*10**-10	#[m] should be 68 nm
		av_speed = calc_av_speed()/time_multiplier*10**-10 #[m/s] should be 13.67 m/s	
		av_free_path_time = free_path/av_speed #[s], 
		Diffusion = 2/3*free_path*av_speed 	#[m^2/s], should be 2e-5 m^2/s
		thermal_conductivity = density*cv*Diffusion	#0.0162 W/(m*K)
		viscosity = density*Diffusion	#should be around 22.7e-6 Pa*s
		# viscosity = 1/3*free_path*c*density	#should be around 22.7e-6 Pa*s
		# thermal_conductivity = cp*(3*R*T)**0.5/(2*(2*mass)*0.5*sigma*N_total)	#0.0162 W/(m*K)
		
		print('num of collisions', len(free_path_list))
		print('density', density, '[kg/m^3]')
		print('free_path', free_path, '[m]')
		print('av_speed', av_speed, '[m/s]')
		print('av_free_path_time', av_free_path_time, '[s]')
		print('Diffusion', Diffusion, 'm^2/s')
		print('thermal_conductivity', thermal_conductivity, '[W/(m*K)]')
		print('viscosity', viscosity, 'Pa*s')

		file = open('results_ex3.txt', 'w')
		file.write('Free path time tau = ' + str(av_free_path_time)+' [s]\n')
		file.write('Diffusion coeff = ' + str(Diffusion)+' [m^2/s]\n')
		file.write('Viscosity = ' + str(viscosity)+' [Pa*s]\n')
		file.write('Thermal conductivity = ' + str(thermal_conductivity)+' [W/(m*K)]\n')
		file.close()
		
		print('Done!')

