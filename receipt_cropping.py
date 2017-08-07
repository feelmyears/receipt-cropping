import argparse
import sys
import time
import datetime

import numpy as np

from crop_vertical import crop_vertical
from utils import get_images, save_image, count_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source',
        type=str,
        help='Directory containing receipt images to crop'
    )
    parser.add_argument(
        '--destination',
        type=str,
        help='Directory to save cropped receipt images'
    )
    parser.add_argument(
        '--scale',
        type=float,
        default=0.5,
        help='Factor by which to scale the images when processing for cropping. 0.5 generally yields best results'
    )
    parser.add_argument(
        '--size',
        type=int,
        help='Height and width of final cropped image. If set, overrides individual height and width arguments'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=299,
        help='Width in pixels of final cropped image'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=299,
        help='Height in pixels of final cropped image'
    )
    parser.add_argument(
        '--vclip',
        type=float,
        default=0.5,
        help='Upper percentage of cropped image to utilize.'
    )
    args = parser.parse_args()
    src = args.source

    dst = args.destination
    if not dst or dst == '':
        dst = src + '_cropped'

    clip = args.vclip
    scale=args.scale
    resize=(args.height, args.width)
    if args.size is not None:
        resize = (args.size, args.size)


    print 'Source Directory:      ', src
    print 'Destination Directory: ', dst
    print 'Scale Factor:          ', scale
    print 'Clip Percentage:       ', clip * 100.0
    print 'Output Image Size:      {}px x {}px'.format(resize[0], resize[1])
    print

    total_images = count_files(src)
    processed_images = 0
    times = []
    remaining_time = ''

    for filename, image in get_images(src):
        sys.stdout.write('Processed {} of {} images [{}]\r'.format(processed_images, total_images, remaining_time))
        sys.stdout.flush()

        t0 = time.time()
        cropped_image = crop_vertical(image, scale=scale, resize=resize, clip=clip)
        save_image(cropped_image, dst + '/' + filename)
        processed_images += 1
        t1 = time.time()
        tot_time = t1 - t0
        times.append(tot_time)

        remaining_time_secs = (total_images - processed_images) / np.mean(times)
        remaining_time = '{} remaining'.format(datetime.timedelta(seconds=int(remaining_time_secs)))

    print 'Processed {} images in {} secs (approx {} secs per image)'.format(total_images, np.sum(times), np.mean(times))

if __name__ == '__main__':
    main()