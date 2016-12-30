from cffi import FFI
import subprocess
import unittest
import os

basepath = os.path.dirname(os.path.abspath(__file__))
libpath = os.path.join(basepath, "lib", "libvector.so")

# if not os.path.isfile(libpath):
#     subprocess.call('/usr/bin/scons libbuild')

with open(os.path.join(basepath, "include", "vector.h")) as f:
    cdef_vector = f.readlines()

cdef_vector = "".join([line for line in cdef_vector if not line.startswith('#')])

ffi = FFI()
ffi.cdef(cdef_vector)
lib = ffi.dlopen(libpath)

class Vector(object):
    def __init__(self, *args, **kwargs):
        if args:
            obj = args[0]
            # if it has x,y,z attributes it probably is the vector_t struct.
            if 'x' in dir(obj) and 'y' in dir(obj) and 'z' in dir(obj):
                cvector = obj
        else:
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            z = kwargs.get('z', 0)
            cvector = ffi.new('vector_t *', [x, y, z])[0]
        super(Vector, self).__setattr__('cvector', cvector)

    def normalize(self):
        return Vector(lib.vector_normalize(self.cvector))

    def dist(self, v):
        return float(lib.vector_distance(self.cvector, v.cvector))

    def dot(self, v):
        return float(lib.vector_dot(self.cvector, v.cvector))

    def get_mag(self):
        return lib.vector_get_magnitude(self.cvector)

    def set_mag(self, size):
        cvector = lib.vector_set_magnitude(self.cvector, size)
        super(Vector, self).__setattr__('cvector', cvector)

    def __setattr__(self, attr, value):
        if attr == 'x':
            self.cvector.x = value
        elif attr == 'y':
            self.cvector.y = value
        elif attr == 'z':
            self.cvector.z = value
        elif attr == 'mag':
            self.set_mag(value)
        else:
            raise AttributeError

    def __getattr__(self, attr):
        if attr == 'x':
            return float(self.cvector.x)
        elif attr == 'y':
            return float(self.cvector.y)
        elif attr == 'z':
            return float(self.cvector.z)
        elif attr == 'mag':
            return float(self.get_mag())
        else:
            raise AttributeError

    def __len__(self):
        return self.mag

    def __add__(self, other):
        if isinstance(other, (int, float)):
            res = lib.vector_sadd(self.cvector, other)
            return Vector(res)
        elif isinstance(other, Vector):
            res = lib.vector_vadd(self.cvector, other.cvector)
            return Vector(res)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            res = lib.vector_ssub(self.cvector, other)
            return Vector(res)
        elif isinstance(other, Vector):
            res = lib.vector_vsub(self.cvector, other.cvector)
            return Vector(res)
        else:
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = lib.vector_smul(self.cvector, other)
            return Vector(res)
        elif isinstance(other, Vector):
            res = lib.vector_vmul(self.cvector, other.cvector)
            return Vector(res)
        else:
            raise TypeError

    def __div__(self, other):
        if isinstance(other, (int, float)):
            res = lib.vector_sdiv(self.cvector, other)
            return Vector(res)
        elif isinstance(other, Vector):
            res = lib.vector_vdiv(self.cvector, other.cvector)
            return Vector(res)
        else:
            raise TypeError

    def __str__(self):
        return str({'x': self.x,
                    'y': self.y,
                    'z': self.z,
                    'mag': self.mag})

    def __repr__(self):
        return {'x': self.x,
                'y': self.y,
                'z': self.z,
                'mag': self.mag}

class TestVector(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector(x=3, y=4)
        self.v2 = Vector(x=1, y=1)
        self.v3 = Vector(x=1, y=2, z=10)

    def testDistance(self):
        dist_shouldbe = ((3 - 1) ** 2 + (4 - 1) ** 2) ** 0.5
        self.assertTrue(int(self.v1.dist(self.v2)) == int(dist_shouldbe))

    def testDotProduct(self):
        va = Vector(x=1, y=3, z=-5)
        vb = Vector(x=4, y=-2, z=-1)
        self.assertTrue(int(va.dot(vb)) == 3)

        # sqrt of the dot of the difference between two vectors
        # is also the distance between two vectors.
        vdiff = va - vb
        self.assertTrue(int(vdiff.dot(vdiff) ** 0.5) == int(va.dist(vb)))

    def testMagnitude(self):
        self.v1.mag = 42
        self.assertTrue(int(self.v1.mag) == 42)
        self.assertTrue(int(len(self.v1)) == 42)

        self.v1.mag = 5
        self.assertTrue(int(self.v1.x) == 3)
        self.assertTrue(int(self.v1.y) == 4)
        self.assertTrue(int(len(self.v1)) == 5)

    def testNormalize(self):
        self.v1 = Vector(x=20, y=30)
        old_mag = self.v1.mag
        self.v1 = self.v1.normalize()
        self.assertTrue(int(self.v1.mag) == 1)
        self.assertTrue(int(self.v1.x) == int(20. / old_mag))
        self.assertTrue(int(self.v1.y) == int(30. / old_mag))


    def testAttributeAccess(self):
        self.assertTrue(int(self.v1.x) == 3)
        self.assertTrue(int(self.v2.y) == 1)
        self.assertTrue(int(self.v3.z) == 10)
        self.assertTrue(int(self.v1.mag) == 5)

        self.v1.x = 10
        self.v1.y = 20
        self.v2.x = 50
        self.v3.mag = 42
        self.assertTrue(int(self.v1.x) == 10)
        self.assertTrue(int(self.v1.y) == 20)
        self.assertTrue(int(self.v2.x) == 50)
        self.assertTrue(int(self.v3.mag) == 42)

        self.v1.x = 4.2
        self.assertTrue(self.v1.x == 4.2)

        with self.assertRaises(TypeError):
            self.v1.x = 'a'

        with self.assertRaises(TypeError):
            self.v1.mag = '1'

    def testAddition(self):
        res = self.v1 + self.v2
        self.assertTrue(res != self.v1)
        self.assertTrue(res != self.v2)
        self.assertTrue(int(res.x) == 4)
        self.assertTrue(int(res.y) == 5)
        self.assertTrue(int(res.z) == 0)

    def testSubtraction(self):
        res = self.v1 - self.v2
        self.assertTrue(res != self.v1)
        self.assertTrue(res != self.v2)
        self.assertTrue(int(res.x) == 2)
        self.assertTrue(int(res.y) == 3)
        self.assertTrue(int(res.z) == 0)

    def testMultiplication(self):
        res = self.v1 * self.v2
        self.assertTrue(res != self.v1)
        self.assertTrue(res != self.v2)
        self.assertTrue(int(res.x) == 3)
        self.assertTrue(int(res.y) == 4)
        self.assertTrue(int(res.z) == 0)

    def testDivision(self):
        self.v2.y = 2
        res = self.v1 / self.v2
        self.assertTrue(res != self.v1)
        self.assertTrue(res != self.v2)
        self.assertTrue(int(res.x) == 3)
        self.assertTrue(int(res.y) == 2)
        self.assertTrue(int(res.z) == 0)


if __name__ == '__main__':
    unittest.main(verbosity=4)