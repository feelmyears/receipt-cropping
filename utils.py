import os
from PIL import Image
import numpy as np
import scipy.misc

def _iter_files(directory):
    """
    Iterates all non-hidden file types in a directory and all subdirectories and yields their path
    """
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for f in filenames:
            if f[0] == '.':
                continue

            yield dirpath + '/' + f

        for d in dirnames:
            for f in _iter_files(directory + '/' + d):
                yield f

def count_files(directory):
    """
    Counts the total number of non-hidden files in a directory and subdirectories
    """
    count = 0
    for _ in _iter_files(directory):
        count += 1
    return count

def get_images(directory):
    """
    Gets all images in a directory (and its subdirectories) of provided types. Assumes all non-hidden files are images
    and converts all images to greyscale.

    Returns the image file's path relative to the base directory and the image as a numpy matrix
    """
    for f in _iter_files(directory):
        yield f[len(directory):], np.asarray(Image.open(f).convert('L'))

def save_image(image, path):
    """
    Saves an image matrix to a path. Creates the necessary directory if the directory does not exist
    """
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    scipy.misc.toimage(image).save(path)




