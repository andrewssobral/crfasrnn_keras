import cv2
import numpy as np

im_input = cv2.imread("input.jpg", cv2.IMREAD_COLOR)
im_output = cv2.imread("output.png", cv2.IMREAD_COLOR)
alpha = 0.5
beta = (1.0 - alpha)
gamma = 0.
img_segment = im_output.copy()
cv2.addWeighted(im_input, alpha, im_output, beta, gamma, img_segment)
#print(img_segment.shape)
rows,cols,ch = img_segment.shape
im_colormap = cv2.imread("colormap.png", cv2.IMREAD_COLOR)
#img_h,img_w,ch = im_colormap.shape
# if img_h > img_w:
#     new_height = 500
#     new_width  = int(new_height * img_w / img_h)
# else:
#     new_width  = 500
#     new_height = int(new_width * img_h / img_w)
#im_colormap = cv2.resize(im_colormap, (new_width, new_height), interpolation = cv2.INTER_CUBIC)
im_colormap = cv2.resize(im_colormap, (cols, rows), interpolation = cv2.INTER_CUBIC)
#print(im_colormap.shape)
img_segment = np.concatenate((img_segment, im_colormap), axis=1)
cv2.imwrite("segmentation.png", img_segment)
