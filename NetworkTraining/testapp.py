'''
Created on Nov 6, 2012

@author: steve
'''
import unittest
import app

class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTwoDimension(self):
        l = range(25)
        twol = app._two_dimension(l)
        expected = [[0,1,2,3,4],
                    [5,6,7,8,9],
                    [10,11,12,13,14],
                    [15,16,17,18,19],
                    [20,21,22,23,24]]
        self.assertSequenceEqual(twol, expected)
        assert twol[3][2] == 17
        
    def testSectionsAsInk(self):
        ''' 0, 3, 6, 10, 24 '''
        sample = [[201, 200, 2, 3, 4, 5, 234, 7, 8, 9],
                  [10, 200, 12, 13, 14, 15, 16, 17, 18, 19],
                  [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                  [30, 31, 32, 233, 34, 35, 36, 37, 38, 39],
                  [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
                  [250, 51, 52, 53, 54, 55, 56, 57, 58, 59],
                  [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
                  [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
                  [80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
                  [90, 91, 92, 93, 94, 95, 96, 97, 201, 99]]
        res = app.sections_as_ink(sample, 25)
        self.assertEquals(res, 
                          [1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()