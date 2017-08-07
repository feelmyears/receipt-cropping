# receipt-cropping
A simple script to crop images of receipts to their vertical edges to reduce surrounding noise and direct focus towards receipt banner images.

## Performance
When run on a proprietary test set of 24,000 images of receipts, the algorithm was able to locate and crop at least one side of the receipt in 99% of images and locate and crop to both sides of the receipt in 85% of images. In the 14% of images in which only one side was located, that side was twice as likely to be the right side of the receipt. This right-side preference may be due to the relative position of a smart phone's camera sensor and flash to the receipt (which are generally located on the left-side of the device). 

Reducing the scale of the image improves runtime but will decrease performance after a certain point.
 
## Dependencies
The script relies upon the following libraries: `scikit-image`, `numpy`, and `PIL`:

```
pip install scikit-image
pip install numpy
pip install pillow
```

## Use
The `receipt_cropping.py` script reads input images from a provided directory (and any subdirectories) and saves the modified images into another directory (while maintaining the internal structure of the input directory). The script accepts the following arguments:

* `--source` **(required)**: Source directory containing receipt images to process
* `--destination` *(optional)*: Destination directory where processed images are to be saved. If not provided, the destination directory will default to *source*_output.
* `--scale` *(optional, default=0.5, float between 0.0 and 1.0)*: Amount to scale images before processing. A lower scale value will improve runtime. A lower scale value can also improve performance up to a certain point, after which performance will greatly suffer.
* `--vclip` *(optional, default=0.5, float between 0.0 and 1.0)*: Percentage of upper image area to include in cropped image. A clip of 0.5 will include the top half of the image while a clip of 0.3 will only include the top 30% of the image.
* `--height` *(optional, default=299, int >= 1)*: Height in pixels of the output image. Ignored when `--size` argument is supplied.
* `--width` *(optional, default=299, int >= 1)*: Width in pixels of the output image. Ignored when `--size` argument is supplied.
* `--size` *(optional, integer >= 1)*: Overrides `--height` and `--width` arguments and sets the output image size to `(height, width) = (size, size)`