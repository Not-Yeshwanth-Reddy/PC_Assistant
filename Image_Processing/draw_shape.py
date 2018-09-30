import cv2


def get_shape(icon_name):
	if icon_name is None:
		return None
	shaped_icon_name = icon_name.split(".")
	shaped_icon_name = str(shaped_icon_name[0]) + "_shape." + str(shaped_icon_name[1])
	img = cv2.imread(icon_name, cv2.IMREAD_GRAYSCALE)
	gray1 = cv2.Canny(img, 70, 50)
	cv2.imwrite(shaped_icon_name, gray1)
	return shaped_icon_name
