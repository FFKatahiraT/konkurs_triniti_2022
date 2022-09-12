import matplotlib.pyplot as plt
from ex3 import particle_force

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
	
force_multiplier = 1
scale_multiplier = 2
r, E, F = particle_force(force_multiplier, scale_multiplier)
start = 400
plotter(r[start:], E[start:], F[start:], 'r [A]', 'Check_ex2_potential')