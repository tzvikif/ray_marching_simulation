import numpy as np
import quaternion
from scipy import linalg

def normalized(v):
    norm = linalg.norm(v)
    if norm > 0:
        return v / norm
    else:
        return v

class ModelTransform:
    def __init__(self):
        self._scale = np.full(3, 1)
        self._position = np.zeros(3)
        self._rotation = np.quaternion(1, 0, 0, 0)
        self._matrix = None
        self._translation_matrix = None
        self._rotation_matrix = None

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = np.asarray(value)
        self._matrix, self._translation_matrix = None, None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = np.asarray(value)
        self._matrix, self._translation_matrix = None, None

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = np.quaternion(value)
        self._matrix, self._rotation_matrix = None, None

    @property
    def matrix(self):
        if self._matrix is None:
            if self._translation_matrix is None:
                sx, sy, sz = self._scale
                x, y, z = self._position
                self._translation_matrix = np.array((
                    (sx,  0,  0, 0),
                    ( 0, sy,  0, 0),
                    ( 0,  0, sz, 0),
                    ( x,  y,  z, 1)))
            if self._rotation_matrix is None:
                self._rotation_matrix = np.identity(4)
                self._rotation_matrix[:3,:3] = \
                    quaternion.as_rotation_matrix(self._rotation)
            R = self._rotation_matrix
            T = self._translation_matrix
            self._matrix = R @ T
        return self._matrix

class ViewTransform:
    def __init__(self):
        self._eye = np.ones(3)
        self.look_at(np.zeros(3), np.array((0,1,0)))

    @property
    def eye(self):
        if self._eye is None:
            self._eye = linalg.inv(self.matrix)[3,:3]
        return self._eye

    @eye.setter
    def eye(self, position):
        self._eye = np.asarray(position)
        _ = self.rotation  # ensure rotation is saved
        self._matrix = None

    @property
    def rotation(self):
        if self._rotation is None:
            self._rotation = \
                quaternion.from_rotation_matrix(
                    self.matrix[:3,:3])
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = np.quaternion(value)
        _ = self.eye  # ensure eye position is saved
        self._matrix = None

    @property
    def matrix(self):
        if self._matrix is None:
            R = self.rotation_matrix
            self._matrix = np.identity(4)
            self._matrix[:3,:3] = R
            self._matrix[3,:3] = [- v.dot(self.eye) for v in R.T]
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value
        self._eye = None
        self._rotation = None

    @property
    def rotation_matrix(self):
        return quaternion.as_rotation_matrix(self.rotation)

    @rotation_matrix.setter
    def rotation_matrix(self, value):
        self.rotation = quaternion.from_rotation_matrix(value)

    def look_at(self, target, up):
        zax = normalized(self.eye - np.asarray(target))
        xax = normalized(np.cross(np.asarray(up), zax))
        yax = np.cross(zax, xax)
        self.rotation_matrix = np.stack((xax, yax, zax), axis=1)

class PerspectiveTransform:
    def __init__(self):
        self._aspect = 4 / 3
        self._fov = 45 * np.pi / 180
        self._near = 0.1
        self._far = 1.
        self._matrix = None

    @property
    def aspect(self):
        return self._aspect

    @aspect.setter
    def aspect(self, value):
        self._aspect = value
        self._matrix = None

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, value):
        self._fov = value
        self._matrix = None

    @property
    def near(self):
        return self._near

    @near.setter
    def near(self, value):
        self._near = value
        self._matrix = None

    @property
    def far(self):
        return self._far

    @far.setter
    def far(self, value):
        self._far = value
        self._matrix = None

    @property
    def matrix(self):
        if self._matrix is None:
            t = np.tan(self._fov / 2) * self._near
            b = - t
            assert abs(t - b) > 0
            l, r = b * self._aspect, t * self._aspect
            assert abs(r - l) > 0
            n, f = self._near, self._far
            assert abs(n - f) > 0
            self._matrix = np.array((
                (  2*n/(r-l),           0,             0,  0),
                (          0,   2*n/(t-b),             0,  0),
                ((r+l)/(r-l), (t+b)/(t-b),   (f+n)/(n-f), -1),
                (          0,           0, 2*(f*n)/(n-f),  0)))
        return self._matrix

class MVPTransform:
    def __init__(self):
        self.model = ModelTransform()
        self.view = ViewTransform()
        self.projection = PerspectiveTransform()

    def matrix(self):
        m = self.model.matrix @ self.view.matrix @ self.projection.matrix
        return m.astype(np.float32)
