import numpy
from PIL import Image

def get_derivative(YLinesIntensities):
	#returns derivative of YLinesIntensities
	DerYLinesIndexes = []
	past_val = YLinesIntensities[1]-YLinesIntensities[0]
	for i in range(1, len(YLinesIntensities)-1):
		if (YLinesIntensities[i+1]-YLinesIntensities[i])*past_val<= 0:
			if past_val > 0:
				DerYLinesIndexes.append(i)
		past_val = YLinesIntensities[i+1]-YLinesIntensities[i]
	return DerYLinesIndexes

def get_MaxIntensities(DerYLinesIndexes, YLinesIntensities, N):
	#returns index of max intensities
	New_array = []
	for i in DerYLinesIndexes:
		New_array.append(YLinesIntensities[i])

	output = []
	for i in range(N):
		output.append(DerYLinesIndexes[New_array.index(max(New_array))])
		del DerYLinesIndexes[New_array.index(max(New_array))]
		del New_array[New_array.index(max(New_array))]
	return output

def get_yLineIntensities_colorless_image(imarray):
	#The same as get_yLineIntensities, but works with
	#colorless images (imarray depth = 2)
	#
	#Takes imarray with depth = 2 (colorless image)
	#Returns list of vertical lines max intensities
	#Each vertical line max intensity is one element
	#of array YLinesIntensities
	YLinesIntensities = []
	for j in range(1, len(imarray[0])):#y
		maxIntensity = imarray[0][j]
		for i in range(len(imarray)):		#x
			if imarray[i][j] > maxIntensity:
				maxIntensity = imarray[i][j]
		YLinesIntensities.append(int(maxIntensity))
	return YLinesIntensities

def get_yLineIntensities(imarray):
	#Takes imarray with depth = 3 (color image)
	#Returns list of vertical lines max intensities
	#Each vertical line max intensity is one element
	#of array YLinesIntensities
	YLinesIntensities = []
	for j in range(1, len(imarray[0])):#y
		maxIntensity = imarray[0][j][0]
		for i in range(len(imarray)):		#x
			if imarray[i][j][0] > maxIntensity:
				maxIntensity = imarray[i][j][0]
		YLinesIntensities.append(int(maxIntensity))
	return YLinesIntensities

def find_signals(imarray, N):
	#finds location of spectra signals
	if type(imarray[0][0]) == numpy.ndarray: #check if image color or colorless 
		YLinesIntensities = get_yLineIntensities(imarray) #(for example, HgSpectra.tif - colored,
	else:	#Dopler.tif - colorless)
		YLinesIntensities = get_yLineIntensities_colorless_image(imarray)
	DerYLinesIndexes = get_derivative(YLinesIntensities) #Getting derivative of YLinesIntensities to determine intensity peaks
	signals = get_MaxIntensities(DerYLinesIndexes, YLinesIntensities, N) #getting maximum intensities using list of peaks
	return signals

def start(name, LinesWavelength):
	im = Image.open(name)
	imarray = numpy.array(im)

	signals = find_signals(imarray, len(LinesWavelength))
	nm_per_px = (LinesWavelength[1] - LinesWavelength[0])/abs(signals[1]-signals[0])

	return nm_per_px

if __name__ == '__main__':
	LinesWavelength = (576.96, 579.07)
	nm_per_px = start('HgSpectra.tif', LinesWavelength)
	# print(*LinesWavelength, 'LinesWavelength')
	# print(*signals, 'signals')
	print(nm_per_px, '[nm/px]')