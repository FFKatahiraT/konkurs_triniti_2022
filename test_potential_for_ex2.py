import matplotlib.pyplot as plt

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
	return r_list, E_list, F_list

def plotter(r_list, E, F, xLabel, yLabel):
	plt.plot(r_list, E)
	plt.scatter(r_list, E, label='Potential')
	plt.plot(r_list, F)
	plt.scatter(r_list, F, label='Force')
	plt.legend(loc='best')
	plt.grid()
	plt.ylabel(yLabel)
	plt.xlabel(xLabel)
	plt.tight_layout()
	plt.show()
	
scale_multiplier = 10
r, E, F = particle_force()
start = 340
plotter(r[start:], E[start:], F[start:], 'r [A]', 'Check_ex2_potential')