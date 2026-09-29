from abc import ABC, abstractmethod
from dataclasses import dataclass
from math import pi, sqrt
from collections import defaultdict


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

    def display_info(self):
        print(
            f"{self} - "
            f"Area: {self.area():.2f}, "
            f"Perimeter: {self.perimeter():.2f}"
        )

    def __add__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented

        return self.area() + other.area()

    def __lt__(self, other):
        if not isinstance(other, Shape):
            return NotImplemented

        return self.area() < other.area()

    def __repr__(self):
        return str(self)


@dataclass
class Rectangle(Shape):
    width: float
    height: float

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle({self.width:g}, {self.height:g})"


@dataclass
class Circle(Shape):
    radius: float

    def area(self):
        return pi * self.radius ** 2

    def perimeter(self):
        return 2 * pi * self.radius

    def __str__(self):
        return f"Circle({self.radius:g})"


@dataclass
class Triangle(Shape):
    a: float
    b: float
    c: float

    def area(self):
        semiperimeter = self.perimeter() / 2

        return sqrt(
            semiperimeter
            * (semiperimeter - self.a)
            * (semiperimeter - self.b)
            * (semiperimeter - self.c)
        )

    def perimeter(self):
        return self.a + self.b + self.c

    def __str__(self):
        return (
            f"Triangle("
            f"{self.a:g}, {self.b:g}, {self.c:g})"
        )


@dataclass
class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def __str__(self):
        return f"Square({self.width:g})"


@dataclass
class Ellipse(Shape):
    a: float
    b: float

    def area(self):
        return pi * self.a * self.b

    def perimeter(self):
        # Ramanujan's approximation
        h = ((self.a - self.b) ** 2) / ((self.a + self.b) ** 2)

        return pi * (self.a + self.b) * (
            1 + (3 * h) / (10 + sqrt(4 - 3 * h))
        )

    def __str__(self):
        return f"Ellipse({self.a:g}, {self.b:g})"


class ShapeCalculator:
    def __init__(self, shapes=None):
        self.shapes = shapes if shapes is not None else []

    def total_area(self):
        return sum(shape.area() for shape in self.shapes)

    def largest_shape(self):
        if not self.shapes:
            return None

        return max(self.shapes, key=lambda shape: shape.area())

    def group_by_type(self):
        groups = defaultdict(list)

        for shape in self.shapes:
            shape_type = type(shape).__name__
            groups[shape_type].append(shape)

        return dict(groups)


def display_shapes(shapes):
    for number, shape in enumerate(shapes, start=1):
        print(
            f"{number}. {shape} - "
            f"Area: {shape.area():.2f}"
        )


def display_groups(groups):
    for shape_type, shapes in groups.items():
        total = sum(shape.area() for shape in shapes)

        print(
            f"{shape_type}s: {len(shapes)} "
            f"(Total area: {total:.2f})"
        )


def main():
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Triangle(3, 4, 5),
        Square(4),
        Ellipse(4, 2),
    ]

    calculator = ShapeCalculator(shapes)

    print("\n📐 SHAPE CALCULATOR 📐")

    print("\nCreated shapes:")
    display_shapes(shapes)

    print(
        f"\n📊 Total area of all shapes: "
        f"{calculator.total_area():.2f}"
    )

    largest = calculator.largest_shape()

    print(
        f"\n🏆 Largest shape: "
        f"{largest} - Area: {largest.area():.2f}"
    )

    print("\n📋 Shapes by type:")

    groups = calculator.group_by_type()
    display_groups(groups)

    rectangle = Rectangle(5, 3)
    circle = Circle(4)

    combined_area = rectangle + circle

    print(
        "\n➕ Combine shapes "
        "(Rectangle + Circle):"
    )
    print(
        f"Total combined area: "
        f"{combined_area:.2f}"
    )

    print("\n📊 Sorting shapes by area (ascending):")

    sorted_shapes = sorted(shapes)

    for shape in sorted_shapes:
        print(
            f"{shape}: "
            f"{shape.area():.2f}"
        )


if __name__ == "__main__":
    main()