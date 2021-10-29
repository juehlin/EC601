# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 23:04:42 2021

@author: nicoddemus

@modified by: Juehao Lin

Check if the image result would be too different from previous run
"""
from PIL import ImageChops, ImageDraw, Image
import pytest
import os
import py.path
import math
import operator

def rms_diff(im1, im2):
    """Calculate the root-mean-square difference between two images
    Taken from: http://snipplr.com/view/757/compare-two-pil-images-in-python/
    """
    h1 = im1.histogram()
    h2 = im2.histogram()

    def mean_sqr(a,b):
        if not a:
            a = 0.0
        if not b:
            b = 0.0
        return (a-b)**2

    return math.sqrt(Image.reduce(operator.add, map(mean_sqr, h1, h2))/(im1.size[0]*im1.size[1]))


class ImageDiff:

    def __init__(self, request):
        self.directory = py.path.local(request.node.fspath.dirname) / request.node.fspath.purebasename
        self.expected_name = (request.node.name + '.png') 
        self.expected_filename = self.directory / self.expected_name

    def check(self, im, max_threshold=2.0):
        __tracebackhide__ = True
        local = py.path.local(os.getcwd()) / self.expected_name
        if not self.expected_filename.check(file=1):
            msg = '\nExpecting image at %s, but it does not exist.\n'
            msg += '-> Generating here: %s'
            im.save(str(local))
            pytest.fail(msg % (self.expected_filename, local))
        else:
            expected = Image.open(str(self.expected_filename))
            rms_value = rms_diff(im, expected)
            if rms_value > max_threshold:
                im.save(str(local))
                msg = '\nrms_value %s > max_threshold of %s.\n'
                msg += 'Obtained image saved at %s'
                pytest.fail(msg % (rms_value, max_threshold, str(local)))

@pytest.fixture
def image_diff(request):        
    return ImageDiff(request)
