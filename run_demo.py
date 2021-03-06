"""
MIT License

Copyright (c) 2017 Sadeep Jayasumana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import util
import sys
import cv2
import numpy as np
from crfrnn_model import get_crfrnn_model_def

def main():
    if(len(sys.argv) > 3):
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        segment_file = sys.argv[3]
    else:
        input_file = "image.jpg"
        output_file = "labels.png"
        segment_file = "segmentation.png"
    print(input_file, output_file)

    # Download the model from https://goo.gl/ciEYZi
    saved_model_path = "crfrnn_keras_model.h5"

    model = get_crfrnn_model_def()
    model.load_weights(saved_model_path)

    img_data, img_h, img_w = util.get_preprocessed_image(input_file)
    probs = model.predict(img_data, verbose=False)[0, :, :, :]
    segmentation = util.get_label_image(probs, img_h, img_w)
    segmentation.save(output_file)
    
    im_input = cv2.imread(input_file, cv2.IMREAD_COLOR)
    img_h,img_w,ch = im_input.shape
    im_output = cv2.imread(output_file, cv2.IMREAD_COLOR)
    im_output = cv2.resize(im_output, (img_w, img_h), interpolation = cv2.INTER_CUBIC)
    alpha = 0.5
    beta = (1.0 - alpha)
    gamma = 0.
    img_segment = im_output.copy()
    cv2.addWeighted(im_input, alpha, im_output, beta, gamma, img_segment)
    rows,cols,ch = img_segment.shape
    im_colormap = cv2.imread("colormap.png", cv2.IMREAD_COLOR)
    im_colormap = cv2.resize(im_colormap, (cols, rows), interpolation = cv2.INTER_CUBIC)
    img_segment = np.concatenate((img_segment, im_colormap), axis=1)
    cv2.imwrite(segment_file, img_segment)

if __name__ == "__main__":
    main()
