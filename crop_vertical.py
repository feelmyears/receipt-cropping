from skimage.exposure import equalize_adapthist
from skimage.filters import threshold_local
from skimage.morphology import dilation, label
from skimage.transform import probabilistic_hough_line
from skimage.feature import canny
from skimage.draw import line_aa

from scipy.misc import imresize
from scipy.ndimage.filters import convolve

import numpy as np

def apply_adapted_thresh(img):
    """
    Applies an localized threshold to the image
    """
    block_size = 101
    adaptive_thresh = threshold_local(img, block_size, offset=0.1)
    img[img < adaptive_thresh] = 0
    img[img >= adaptive_thresh] = 1
    return img

def split_segments_vertically(segments, img_shape):
    """
    Splits line segments into left and right groups
    """
    left, right = [], []
    split = img_shape[1] // 2
    for (p1, p2) in segments:
        if p1[0] < split and p2[0] < split:
            left.append((p1, p2))
        elif p1[0] > split and p1[0] > split:
            right.append((p1, p2))

    return left, right

def find_longest_line(lines, img_shape):
    """
    Finds the curve with the longest vertical project in a 2D bitmap
    """
    _img = np.zeros(img_shape)
    _img = draw_lines(_img, lines)
    vertical_kernel = np.ones((100, 5))
    _img = dilation(_img, vertical_kernel)
    labeled, num_segments = label(_img, return_num=True)

    lengths = []
    for i in range(1, num_segments + 1):
        y, x = np.where(labeled == i)
        lengths.append((abs(max(y) - min(y)), max(y), min(y), int(np.mean(x))))

    lengths = sorted(lengths, reverse=True, key=lambda x: x[0])
    return lengths[0] if len(lengths) else None

def draw_lines(img, lines):
    """
    Draws a set of lines onto a 2D bitmap
    """
    for l in lines:
        rr, cc, val = line_aa(l[0][1], l[0][0], l[1][1], l[1][0])
        img[rr, cc] = 1

    return img

def crop_vertical(img, scale=0.5, resize=(299,299), clip=0.5):
    """
    Attempts to crop a receipt image to the sides of the receipt. Will crop either neither, left, right, or both sides.

    :param img:     Receipt image to crop (greyscale numpy array)
    :param scale:   Amount to scale image before processing. Reductions in scale improve runtime and performance (to a certain point)
    :param resize:  Dimensions for final cropped image
    :param clip:    Percentage of upper image area to include in cropped image. A clip of 0.5 will include the top half
                    area of the image while a clip of 0.3 will only include the top 30% of the image.
    """
    img = imresize(img, scale)
    _img = np.copy(img)

    _img = equalize_adapthist(_img)
    _img = apply_adapted_thresh(_img)

    size = 7
    weights = np.ones((size,size))
    _img = convolve(_img, weights)
    _img[_img < size ** 2] = 0
    _img[_img >= size ** 2] = 1

    _img = canny(_img, sigma=5)

    theta_offset = 0.15
    n_buckets = 20
    theta = np.linspace(-theta_offset, theta_offset, n_buckets)
    lines = probabilistic_hough_line(_img, threshold=10, line_length=30, line_gap=5, theta=theta)

    left, right = split_segments_vertically(lines, img.shape)

    longest_left = find_longest_line(left, img.shape)
    longest_right = find_longest_line(right, img.shape)

    min_length = 0.5
    left_crop = 0
    right_crop = img.shape[1]

    if longest_left is not None and longest_left[0] >= img.shape[0] * min_length:
        left_crop = longest_left[-1]

    if longest_right is not None and longest_right[0] >= img.shape[0] * min_length:
        right_crop = longest_right[-1]


    _img = img[:int(img.shape[0]*clip), left_crop:right_crop]
    if resize:
        _img = imresize(_img, resize)

    return _img