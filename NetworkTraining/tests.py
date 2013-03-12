'''
Created on Nov 6, 2012

@author: steve
'''
import unittest
import image_ops
import postprocess
import pygame

class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTwoDimension(self):
        l = range(25)
        twol = image_ops.two_dimension(l)
        expected = [[0,1,2,3,4],
                    [5,6,7,8,9],
                    [10,11,12,13,14],
                    [15,16,17,18,19],
                    [20,21,22,23,24]]
        self.assertSequenceEqual(twol, expected)
        assert twol[3][2] == 17
        
    def testSectionsAsInk(self):
        ''' 0, 3, 6, 10, 24 '''
        sample = [[251, 250, 2, 3, 4, 5, 254, 7, 8, 9],
                  [10, 250, 12, 13, 14, 15, 16, 17, 18, 19],
                  [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                  [30, 31, 32, 253, 34, 35, 36, 37, 38, 39],
                  [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
                  [250, 51, 52, 53, 54, 55, 56, 57, 58, 59],
                  [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
                  [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
                  [80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
                  [90, 91, 92, 93, 94, 95, 96, 97, 251, 99]]
        res = image_ops.sections_as_ink(sample, 25)
        self.assertEquals(res, 
                          [1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
    
    def testImageResizing(self):
        ''' Just resize an image and open larger and smaller versions, have
        to be visual inspections. Also need to all be 28x28. '''
        datas = []
        for pixels in postprocess.pixel_datas():
            datas.append(pixels)
            if len(datas) > 4:
                break
        for each in datas:
            # Splice because first item is answer
            surface = postprocess.make_surface_from(each[1:])
            smaller_surface = postprocess.resize(surface, -0.3)
            larger_surface = postprocess.resize(surface, 0.3)
            assert surface.get_size() == (28, 28)
            assert smaller_surface.get_size() == (28, 28)
            assert larger_surface.get_size() == (28, 28)
            
            # Wish I could find a way to open a surface without saving it??
            pygame.image.save(surface, '/Users/steve/Dev/scrawl/NetworkTraining/testdata/%d.jpg' %(each[0]))
            pygame.image.save(smaller_surface, '/Users/steve/Dev/scrawl/NetworkTraining/testdata/%d_smaller.jpg' %(each[0]))
            pygame.image.save(larger_surface, '/Users/steve/Dev/scrawl/NetworkTraining/testdata/%d_larger.jpg' %(each[0]))

    def testImageRotation(self):
        datas = []
        for pixels in postprocess.pixel_datas():
            datas.append(pixels)
            if len(datas) > 4:
                break
        for each in datas:
            surface = postprocess.make_surface_from(each[1:])
            left_surface = postprocess.rotate(surface, 10)
            right_surface = postprocess.rotate(surface, -10)
            assert surface.get_size() == (28, 28)
            assert left_surface.get_size() == (28, 28)
            assert right_surface.get_size() == (28, 28)
            pygame.image.save(left_surface, '/Users/steve/Dev/scrawl/NetworkTraining/testdata/%d_left.jpg' %(each[0]))
            pygame.image.save(right_surface, '/Users/steve/Dev/scrawl/NetworkTraining/testdata/%d_right.jpg' %(each[0]))
        
    def testSurfaceToPixels(self):
        ''' If we read pixels, make an image, and write pixels, should be back
        to where we started. '''
        for orig_pix in postprocess.pixel_datas():
            break
        surface = postprocess.make_surface_from(orig_pix[1:])
        new_pix = postprocess.surface_as_pixels(surface)
        self.assertEquals(orig_pix[1:], new_pix)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()