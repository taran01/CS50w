import unittest

from prime import is_prime

class Tests(unittest.TestCase):

    def test1(self):
        """Check if 1 is not prime."""
        self.assertFalse(is_prime(1))

    def test2(self):
        """Check if 2 is prime."""
        self.assertTrue(is_prime(2))

    def test8(self):
        """Check if 8 is not prime."""
        self.assertFalse(is_prime(8))

    def test11(self):
        """Check if 11 is prime."""
        self.assertTrue(is_prime(11))

    def test25(self):
        """Check if 25 is not prime."""
        self.assertFalse(is_prime(25))

    def test28(self):
        """Check if 28 is not prime."""
        self.assertFalse(is_prime(28))

if __name__ == "__main__":
    unittest.main()
