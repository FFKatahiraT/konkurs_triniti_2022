import matplotlib.pyplot as plt

def read_data(name):
	file = open(name, 'r')
	data = file.read().split('\n')
	r, val = [], []
	for line in data:
		if line!='':
			if line[0]!='%':
				r_temp, val_temp = line.split(',')
				r.append(float(r_temp))
				val.append(float(val_temp)+1054.09745)
	return r, val

def change_parameter(Multiply_parameter, val, rate=1):
	'''Multiplies or derives parameter value
		rate forces parameter change value'''
	if Multiply_parameter:
		val *= (1+1e-5*rate)
	else:
		val /= (1+1e-5*rate)
	return val

def solve_eq_dF_dsigma(sigma, eps):
	counter = 0 #In case of abscense of solution, calculation should be aborted
	Multiply_parameter = True
	dF_dsigma = 100
	print('-------DEBUG dF_dsigma-------')
	print('dF_dsigma', 'sigma')
	while abs(dF_dsigma) > errorVal*1e-2:
		dF_dsigma_prev = dF_dsigma
		dF_dsigma = 0
		for i in range(len(r)):
			dF_dsigma += (E[i]-4*eps*((sigma/r[i])**12-(sigma/r[i])**6))*(12*sigma**11/r[i]**12-6*sigma**5/r[i]**6)
		
		print(dF_dsigma, sigma)
		if abs(dF_dsigma) - abs(dF_dsigma_prev) > 0:
				Multiply_parameter = not Multiply_parameter	#change direction of parameter selection
				print('Multiply_parameter was changed')
		#else keep moving
		sigma = change_parameter(Multiply_parameter, sigma)
	
		counter += 1
		if counter > 10**3:
			print('Runout of calc steps. sigma: ',sigma)
			break
	print('-------END OF dF_dsigma-------')
	return sigma

def solve_eq_dF_deps(sigma, eps):
	counter = 0 #In case of abscense of solution, calculation should be aborted
	Multiply_parameter = True
	dF_deps = 100
	print('-------DEBUG dF_deps-------')
	print('dF_deps', 'eps')
	while abs(dF_deps) > errorVal*1e-2:
		dF_deps_prev = dF_deps
		dF_deps = 0
		for i in range(len(r)):
			tau = (sigma/r[i])**12-(sigma/r[i])**6
			dF_deps += E[i]*tau-4*eps*tau**2
		
		print(dF_deps, eps)
		if abs(dF_deps) - abs(dF_deps_prev) > 0:
			Multiply_parameter = not Multiply_parameter	#change direction of parameter selection
			print('Multiply_parameter was changed')
		#else keep moving
		eps = change_parameter(Multiply_parameter, eps, rate=3e2)
		
		counter += 1
		if counter > 10**3:
			print('Runout of calc steps. eps: ',eps)
			break
	print('-------END OF dF_deps-------')
	return eps

def least_square_method():
	sigma, eps = 3.8, 1200
	sigma_prev, eps_prev = 0, 0
	print('Least square method')
	print('sigma', 'eps')
	while abs(sigma - sigma_prev)/sigma > errorVal and abs(eps - eps_prev)/eps > errorVal:
		sigma_prev, eps_prev = sigma, eps
		sigma = solve_eq_dF_dsigma(sigma, eps)
		eps = solve_eq_dF_deps(sigma, eps)
		print(sigma, eps)
	return sigma, eps

def approximated_curve(r, sigma, eps):
	y = []
	for x in r:
		y.append(4*eps*((sigma/x)**12-(sigma/x)**6))
	return y

def plotter(r_list, Func_list, xLabel, yLabel, Label, xlog):
	linestyle=['solid', 'dotted', 'dashed', 'dashdot', (0, (5,10)), (0, (5,1)), (0, (3,10,1,10)), (0, (3,1,1,1))]
	pointstyle = ('o', 'v', '^', '<', '>', 's', 'p')
	plt.rcParams.update({'font.size': 14})
	for i in (range(len(r_list))):
		plt.plot(r_list[i], Func_list[i], linestyle=linestyle[i])
		plt.scatter(r_list[i], Func_list[i], label=Label[i], marker=pointstyle[i])
	plt.legend(loc='best')
	plt.grid()
	plt.ylabel(yLabel)
	if xlog: plt.xscale('log') 
	plt.xlabel(xLabel)
	plt.tight_layout()
	plt.savefig(yLabel[:11]+'.svg')
	plt.close()
	
	
# processing('data.csv', 'E [Ha]', xlog=False)
r, E = read_data('data.csv')
errorVal = 0.001
sigma, eps = least_square_method()
print('solution found')
print('sigma', 'eps')
print(sigma, eps)

# eps = 1054.09794929	#manual eps&sigma
# sigma = 3.3943241161146926
# 3.392176105163491 sigma 0.0005005018809095022 eps
r_approx = []
for i in range(1,80):
	r_approx.append(3.2+i**2/1000) 	#1 -- 10/3.2
y = approximated_curve(r_approx,sigma, eps)

Label = ('Data', 'Approximation')
plotter((r,r_approx), (E, y), 'r [A]', 'E [Ha]', Label,xlog=False)