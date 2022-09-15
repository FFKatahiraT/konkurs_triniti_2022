import numpy
from PIL import Image
import ex2_prac

#getting nm/px scale
LinesWavelength = (576.96, 579.07)
nm_per_px = ex2_prac.start('HgSpectra.tif', LinesWavelength)

im = Image.open('Dopler.tif')
imarray = numpy.array(im)

#getting px coordinates of vertical lines with spectra signals
signals = ex2_prac.find_signals(imarray, 2)
# print(signals, 'signals')
DoplerShift = abs(signals[1]-signals[0])*nm_per_px #calc Doplee shift
print('Dopler shift:', DoplerShift, '[nm]')