"""Function validation tests."""

import unittest

import numpy as np
import tensorflow as tf

from optfuncs import numpy_functions as npf
from optfuncs import tensorflow_functions as tff

# TODO: Check how to run R implementation in this test
# TODO: Add gradient test

array = [1, 2, 3, 4]
array_lookup = {
  "Ackley": 8.43469444443746497,
  "Griewank": 1.00187037800320189,
  "Rastrigin": 30.0,
  "Levy": 2.76397190019909811,
  "Rosenbrock": 2705.0,
  "Zakharov": 50880.0,
  "SumSquares": 100.0,
  "Sphere": 30.0,
  "RotatedHyperEllipsoid": 50.0,
  "DixonPrice": 4230.0,
}

zeros = [0, 0, 0, 0]
zero_lookup = {
  "Ackley": 4.44089209850062616e-16,
  "Griewank": 0.0,
  "Rastrigin": 0.0,
  "Levy": 0.897533662350923467,
  "Rosenbrock": 3.0,
  "Zakharov": 0.0,
  "SumSquares": 0.0,
  "Sphere": 0.0,
  "RotatedHyperEllipsoid": 0.0,
  "DixonPrice": 1.0,
}


class TestNumpyFunctions(unittest.TestCase):
  batch_size = 2  # batch size of array in multiple input testing
  dtype = np.float64

  @classmethod
  def setUpClass(cls) -> None:
    cls.array = np.array(array, cls.dtype)
    cls.batch = cls.array[None].repeat(cls.batch_size, axis=0)
    cls.zero = np.array(zeros, cls.dtype)

  @classmethod
  def tearDownClass(cls) -> None:
    del cls.array
    del cls.zero
    del cls.batch

  def default_test(self, f: npf.NumpyFunction):
    array_result = np.array(array_lookup[f.name], self.dtype)
    batch_result = np.array(array_result).repeat(self.batch_size)
    zero_result = np.array(zero_lookup[f.name], self.dtype)

    # Test default value [1,2,3,4]
    result = f(self.array)
    self.assertEqual(result, array_result)

    # Test batch of default value [[1,2,3,4],[1,2,3,4], ...]
    result = f(self.batch)
    self.assertTrue(np.array_equal(result, batch_result))
    self.assertEqual(result.shape, batch_result.shape)

    result = f(self.zero)
    self.assertEqual(result, zero_result)

    # Testing shape and dtype
    self.assertEqual(result.shape, zero_result.shape)
    self.assertEqual(result.dtype, zero_result.dtype)

  def test_ackley(self):
    self.default_test(npf.Ackley())

  def test_griewank(self):
    self.default_test(npf.Griewank())

  def test_rastrigin(self):
    self.default_test(npf.Rastrigin())

  def test_levy(self):
    self.default_test(npf.Levy())

  def test_rosenbrock(self):
    self.default_test(npf.Rosenbrock())

  def test_zakharov(self):
    self.default_test(npf.Zakharov())

  def test_sum_squares(self):
    self.default_test(npf.SumSquares())

  def test_sphere(self):
    self.default_test(npf.Sphere())

  def test_rotated_hyper_ellipsoid(self):
    self.default_test(npf.RotatedHyperEllipsoid())

  def test_dixon_price(self):
    self.default_test(npf.DixonPrice())


class TestTensorflowFunctions(unittest.TestCase):
  batch_size = 10  # batch size of array in multiple input testing
  dtype = tf.float64

  @classmethod
  def setUpClass(cls) -> None:
    cls.array = tf.constant(array, dtype=cls.dtype)
    cls.batch = tf.repeat(cls.array[None], cls.batch_size, 0)
    cls.zeros = tf.constant(zeros, dtype=cls.dtype)

  @classmethod
  def tearDownClass(cls) -> None:
    del cls.array
    del cls.zeros
    del cls.batch

  # Get batch expected result from array expected result
  def batch_result(self, array_result: tf.Tensor) -> tf.Tensor:
    return tf.repeat(tf.expand_dims(array_result, 0), self.batch_size, 0)

  # Test a given function
  def default_test(self, f: tff.TensorflowFunction):
    array_result = tf.constant(array_lookup[f.name], self.dtype)
    batch_result = self.batch_result(array_result)
    zero_result = tf.constant(zero_lookup[f.name], self.dtype)

    # Test default value [1,2,3,4]
    result = f(self.array)
    tf.debugging.assert_near(result, array_result)

    # Test batch of default value [[1,2,3,4],[1,2,3,4], ...]
    result = f(self.batch)
    self.assertTrue(tf.reduce_all(result == batch_result))
    self.assertEqual(result.shape, batch_result.shape)

    result = f(self.zeros)
    tf.debugging.assert_near(result, zero_result)

    # Testing Tracing
    f = tf.function(f)

    # Test default value [1,2,3,4] after Tracing
    result = f(self.array)
    tf.debugging.assert_near(result, array_result)

    # Testing shape and dtype
    self.assertEqual(result.shape, array_result.shape)
    self.assertEqual(result.dtype, array_result.dtype)

  def tf_function_test(self, f: tff.TensorflowFunction):
    f.enable_tf_function()
    self.default_test(f)
    f.disable_tf_function()

  def test_ackley(self):
    self.default_test(tff.Ackley())
    self.tf_function_test(tff.Ackley())

  def test_griewank(self):
    self.default_test(tff.Griewank())
    self.tf_function_test(tff.Griewank())

  def test_rastrigin(self):
    self.default_test(tff.Rastrigin())
    self.tf_function_test(tff.Rastrigin())

  def test_levy(self):
    self.default_test(tff.Levy())
    self.tf_function_test(tff.Levy())

  def test_rosenbrock(self):
    self.default_test(tff.Rosenbrock())
    self.tf_function_test(tff.Rosenbrock())

  def test_zakharov(self):
    self.default_test(tff.Zakharov())
    self.tf_function_test(tff.Zakharov())

  def test_sum_squares(self):
    self.default_test(tff.SumSquares())
    self.tf_function_test(tff.SumSquares())

  def test_sphere(self):
    self.default_test(tff.Sphere())
    self.tf_function_test(tff.Sphere())

  def test_rotated_hyper_ellipsoid(self):
    self.default_test(tff.RotatedHyperEllipsoid())
    self.tf_function_test(tff.RotatedHyperEllipsoid())

  def test_dixon_price(self):
    self.default_test(tff.DixonPrice())
    self.tf_function_test(tff.DixonPrice())


if __name__ == "__main__":
  unittest.main()