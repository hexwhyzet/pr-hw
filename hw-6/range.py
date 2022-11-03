def test_str():
    rng1 = Range()
    assert str(rng1) == "[empty]"
    rng2 = Range(-5, 3)
    assert str(rng2) == "[-5:3]"


def test_is_empty():
    rng1 = Range(1, 1)
    assert not rng1.is_empty
    rng2 = Range(1, 5)
    assert not rng2.is_empty
    rng3 = Range()
    assert rng3.is_empty


def test_contains():
    rng = Range(1, 5)
    assert rng.contains(3)
    assert rng.contains(1)
    assert not rng.contains(-1)


def test_equality():
    rng1 = Range(0, 5)
    rng2 = Range(0, 5)
    rng3 = Range(0, 4)
    rng4 = Range(1, 5)

    assert rng1 == rng2
    assert rng1 != rng3
    assert rng1 != rng4


def test_intersects():
    rng1 = Range(0, 3)
    rng2 = Range(2, 4)
    rng3 = Range(4, 5)
    rng4 = Range(-1, 10)
    rng5 = Range(-5, -1)

    assert rng1.intersects(rng2)
    assert rng2.intersects(rng3)
    assert rng1.intersects(rng4)
    assert not rng1.intersects(rng5)


def test_conjunction():
    rng1 = Range(0, 10)
    rng2 = Range(-5, 5)

    assert (rng1 & rng2) == Range(0, 5)


def test_disjunction():
    rng1 = Range(0, 10)
    rng2 = Range(-5, 5)

    assert (rng1 | rng2) == Range(-5, 10)


def test_include():
    rng1 = Range(0, 10)
    rng2 = Range(0, 3)
    rng3 = Range(7, 10)
    rng4 = Range(4, 8)
    rng5 = Range(-2, 2)
    rng6 = Range(-5, -4)

    assert rng1.includes(rng2)
    assert rng1.includes(rng3)
    assert rng1.includes(rng4)
    assert not rng1.includes(rng5)
    assert not rng1.includes(rng6)


def test_list():
    rng = Range(-3, 3)
    assert rng.list_points() == [-3, -2, -1, 0, 1, 2, 3]


def test_max_min():
    rng = Range(-2, 6)
    assert rng.min() == -2
    assert rng.max() == 6


class Range:
    is_empty: bool
    left: int
    right: int

    def __init__(self, left=None, right=None):
        assert (left is None) == (right is None)
        if left is None:
            self.is_empty = True
            return
        assert right >= left
        self.is_empty = False
        self.left = left
        self.right = right

    def __repr__(self):
        if self.is_empty:
            return "Range [empty]"
        return f"Range [{self.left}:{self.right}]"

    def __str__(self):
        if self.is_empty:
            return "[empty]"
        return f"[{self.left}:{self.right}]"

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def contains(self, point) -> bool:
        return self.left <= point <= self.right

    def intersects(self, other) -> bool:
        return max(self.left, other.left) <= min(self.right, other.right)

    def includes(self, inner) -> bool:
        return self.left <= inner.left and inner.right <= self.right

    def __and__(self, other):
        if self.is_empty or other.is_empty:
            return Range()
        if not self.intersects(other):
            return Range()
        return Range(max(self.left, other.left), min(self.right, other.right))

    def __or__(self, other):
        if self.is_empty or other.is_empty:
            return Range()
        if not self.intersects(other):
            return Range()
        return Range(min(self.left, other.left), max(self.right, other.right))

    def list_points(self) -> list[int]:
        return list(range(self.left, self.right + 1))

    def max(self):
        return self.right

    def min(self):
        return self.left
