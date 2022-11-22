import os
import sys
import random
import itertools
import colorsys
import cv2
import numpy as np
from skimage.measure import find_contours
import matplotlib.pyplot as plt
from matplotlib import patches,  lines
from matplotlib.patches import Polygon
import utils
from config import Config


def display_images(images, titles=None, cols=4, cmap=None, norm=None,
                   interpolation=None):

    titles = titles if titles is not None else [""] * len(images)
    rows = len(images) // cols + 1
    plt.figure(figsize=(14, 14 * rows // cols))
    i = 1
    for image, title in zip(images, titles):
        plt.subplot(rows, cols, i)
        plt.title(title, fontsize=9)
        plt.axis('off')
        plt.imshow(image.astype(np.uint8), cmap=cmap,
                   norm=norm, interpolation=interpolation)
        i += 1
    plt.show()



def random_colors(N, bright=True, opencv=True):
    brightness = 255 if bright else 180
    if opencv is False:
        brightness = 1 if bright else 0.7
    hsv = [(i / N + 1, 1, brightness) for i in range(N + 1)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

def get_mask_contours(mask):
    #mask = masks[:, :, i]
    # Mask Polygon
    # Pad to ensure proper polygons for masks that touch image edges.
    contours_mask = []
    padded_mask = np.zeros(
        (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
    padded_mask[1:-1, 1:-1] = mask
    contours = find_contours(padded_mask, 0.5)
    for verts in contours:
        # Subtract the padding and flip (y, x) to (x, y)
        verts = np.fliplr(verts) - 1
        contours_mask.append(np.array(verts, np.int32))
    return contours_mask


def apply_mask(image, mask, color):
    """Apply the given mask to the image.
    """
    for c in range (3):
        image[:,:,c] = np.where((mask != 1),image[:,:,c],0)   
    return image


def display_instances(image, masks, class_names, title="",
                      figsize=(16, 16), ax=None,
                      show_mask=True, show_bbox=True,
                      colors=None, captions=None):

    # If no axis is passed, create one and automatically call show()
    _, ax = plt.subplots(1, figsize=figsize)


    # Generate random colors
    color = [0,0,0]

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    for i in range(masks.shape[2]):
        # Mask
        mask = masks[:, :, i]
        masked_image = apply_mask(masked_image, mask, color)



        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)
    ax.imshow(masked_image.astype(np.uint8))
    plt.savefig("output.jpg")



