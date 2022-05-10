import cv2

images = {
	"toast_4x.png": (1, 4)
}


for path in images:
	print(path, images)
	img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
	dimensions = img.shape

	for x in range(images[path][0]):
		for y in range(images[path][1]):
			print(x, y)
			crop_img = img[
				y*int(dimensions[0]/images[path][1]):y*int(dimensions[0]/images[path][1])+int(dimensions[0]/images[path][1]),
				x*int(dimensions[1]/images[path][0]):x*int(dimensions[1]/images[path][0])+int(dimensions[1]/images[path][0])
			]
			cv2.imwrite(f"{x}_{y}_{path}", crop_img)
			cv2.waitKey(0)