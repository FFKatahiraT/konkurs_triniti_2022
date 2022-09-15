import numpy
from PIL import Image

# im = Image.open('HgSpectra.tif')
im = Image.open('Dopler.tif')
imarray = numpy.array(im)
for i in range(len(imarray)):
	# imarray[i][745][0] = 255	#imarray[y][x][R G B]
	imarray[i][66] = 255	#imarray[y][x][I]
	imarray[i][97] = 255	#imarray[y][x][I]
print(len(imarray), 'len imarray, depth=1')
print(len(imarray[0]), 'len imarray, depth=2')
print(len(imarray[0])==len(imarray[10]), 'Depth 2 len the same')
print(imarray[10][10], 'imarray, depth=3')

im = Image.fromarray(imarray)
im.save('test.tif')