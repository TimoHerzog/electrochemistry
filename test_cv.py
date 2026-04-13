import unittest
import numpy as np
import cyclic_voltammetry as cv

class test_cv(unittest.TestCase):
    # init
    def test_init_differenLen(self):
        self.assertRaises(ValueError, cv.CV, np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8, 0.9]))

    # getPotentialAt
    def test_getPotentialAt_correctValue(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        self.assertEqual(testInst.getPotentialAt(0.65, 0.05), 0.2)

    def test_getPotentialAt_farValue(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        self.assertRaises(ValueError, testInst.getPotentialAt, 0.65, 0)

    # getCurrentAt
    def test_getCurrentAt_correctValue(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        self.assertEqual(testInst.getCurrentAt(0.16, 0.4), 0.6) 

    def test_getCurrentAt_farValue(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        self.assertRaises(ValueError, testInst.getCurrentAt, 0.16, 0)

    # iRCompensate
    def test_iRCompensate(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        compensated = testInst.iRCompensate(1.57)
        self.assertTrue(
            np.allclose(compensated.volts, np.array([-0.528, -0.742, -0.956]))
        )

    def test_iRCompensate_negative(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        self.assertRaises(ValueError, testInst.iRCompensate, -1.57)


    # shiftPotential
    def test_shiftPotential_negative(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        shifted = testInst.shiftPotential(-0.8)
        self.assertTrue(
            np.allclose(shifted.volts, np.array([-0.7, -0.6, -0.5]))
        )
        self.assertTrue(
            np.allclose(shifted.amps, np.array([0.4, 0.6, 0.8]))
        )

    def test_shiftPotential_positive(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        shifted = testInst.shiftPotential(0.3)
        self.assertTrue(
            np.allclose(shifted.volts, np.array([0.4, 0.5, 0.6]))
        )
        self.assertTrue(
            np.allclose(shifted.amps, np.array([0.4, 0.6, 0.8]))
        )

    def test_shiftPotential_same(self):
        testInst = cv.CV(np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.6, 0.8]))
        shifted = testInst.shiftPotential(0)
        self.assertTrue(
            np.allclose(shifted.volts, np.array([0.1, 0.2, 0.3]))
        )
        self.assertTrue(
            np.allclose(shifted.amps, np.array([0.4, 0.6, 0.8]))
        )


    # afterLeftVertex
    def test_afterLeftVertex(self):
        testInst = cv.CV(
            np.array([-0.5, 1, 5, -4, -7, -3.5, -0.5]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertTrue( np.array_equal(testInst.afterLeftVertex().volts, np.array([-7, -3.5, -0.5])) )
        self.assertTrue( np.array_equal(testInst.afterLeftVertex().amps, np.array([5,6,7])) )

    def test_afterLeftVertex_edge(self):
        testInst = cv.CV(
            np.array([-3.5, -2, 0, 1, -0.5, -2, -3]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertTrue( np.array_equal(testInst.afterLeftVertex().volts, np.array([-3.5, -2, 0, 1, -0.5, -2, -3])) )
        self.assertTrue( np.array_equal(testInst.afterLeftVertex().amps, np.array([1,2,3,4,5,6,7])) )

    def test_afterLeftVertex_empty(self):
        testInst = cv.CV(
            np.array([-3, -2, 0, 1, -0.5, -2, -3.5]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertRaises(ValueError, testInst.afterLeftVertex)

    def test_afterLeftVertex_ambigious(self):
        testInst = cv.CV(
            np.array([-3, -2, 0, 1, -0.5, -2, -3]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertRaises(ValueError, testInst.afterLeftVertex)


    # beforeLeftVertex
    def test_beforeLeftVertex(self):
        testInst = cv.CV(
            np.array([-0.5, 1, 5, -4, -7, -3.5, -0.5]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertTrue( np.array_equal(testInst.beforeLeftVertex().volts, np.array([-0.5, 1, 5, -4, -7])) )
        self.assertTrue( np.array_equal(testInst.beforeLeftVertex().amps, np.array([1,2,3,4,5])) )

    def test_beforeLeftVertex_edge(self):
        testInst = cv.CV(
            np.array([-3, -2, 0, 1, -0.5, -2, -3.5]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertTrue( np.array_equal(testInst.beforeLeftVertex().volts, np.array([-3, -2, 0, 1, -0.5, -2, -3.5])) )
        self.assertTrue( np.array_equal(testInst.beforeLeftVertex().amps, np.array([1,2,3,4,5,6,7])) )

    def test_beforeLeftVertex_empty(self):
        testInst = cv.CV(
            np.array([-3.5, -2, 0, 1, -0.5, -2, -3]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertRaises(ValueError, testInst.beforeLeftVertex)

    def test_beforeLeftVertex_ambiguous(self):
        testInst = cv.CV(
            np.array([-1, -2, -3, 0, -3, -2]),
            np.array([1,2,3,4,5,6])
        )
        self.assertRaises(ValueError, testInst.beforeLeftVertex)


    # afterRightVertex
    def test_afterRightVertex(self):
        testInst = cv.CV(
            np.array([-0.5, 1, 4, 7, 3.5, -1, -0.5]),
            np.array([1,2,3,4,5,6,7])
        )
        self.assertTrue( np.array_equal(testInst.afterRightVertex().volts, np.array([7, 3.5, -1, -0.5])) )
        self.assertTrue( np.array_equal(testInst.afterRightVertex().amps, np.array([4,5,6,7])) )

    def test_afterRightVertex_edge(self):
        testInst = cv.CV(
            np.array([4, 1, -0.5, -2, -3]),
            np.array([1,2,3,4,5])
        )
        self.assertTrue( np.array_equal(testInst.afterRightVertex().volts, np.array([4, 1, -0.5, -2, -3])) )
        self.assertTrue( np.array_equal(testInst.afterRightVertex().amps, np.array([1,2,3,4,5])) )

    def test_afterRightVertex_empty(self):
        testInst = cv.CV(
            np.array([-3, -2, 0, 1]),
            np.array([1,2,3,4])
        )
        self.assertRaises(ValueError, testInst.afterRightVertex)

    def test_afterRightVertex_ambigious(self):
        testInst = cv.CV(
            np.array([-2, 0, 1, -0.5, 1, -3]),
            np.array([1,2,3,4,5,6])
        )
        self.assertRaises(ValueError, testInst.afterRightVertex)