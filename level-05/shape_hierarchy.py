'''
🟡 Mid Level (2 Questions)
Q3: The Shape Hierarchy with Calculators (Mid)

Create a comprehensive shape hierarchy with area/perimeter calculators.

Requirements:

    Create an abstract base class Shape with:

        Abstract methods: area(), perimeter()

        Concrete method: display_info()

    Create concrete classes:

        Rectangle(width, height)

        Circle(radius)

        Triangle(a, b, c)

        Square(side) (inherits from Rectangle)

        Ellipse(a, b)

    Create a ShapeCalculator that:

        Calculates total area of list of shapes

        Finds largest shape

        Groups shapes by type

    Use dataclasses for simple shapes

    Implement magic methods:

        __add__ to combine shapes (total area)

        __lt__ to compare shapes by area

        __repr__ for debugging

Sample Output:
text

📐 SHAPE CALCULATOR 📐

Created shapes:
1. Rectangle(5, 3) - Area: 15.00
2. Circle(4) - Area: 50.27
3. Triangle(3, 4, 5) - Area: 6.00
4. Square(4) - Area: 16.00
5. Ellipse(4, 2) - Area: 25.13

📊 Total area of all shapes: 112.40

🏆 Largest shape: Circle(4) - Area: 50.27

📋 Shapes by type:
Rectangles: 2 (Total area: 31.00)
Circles: 1 (Total area: 50.27)
Triangles: 1 (Total area: 6.00)
Ellipses: 1 (Total area: 25.13)

➕ Combine shapes (Rectangle + Circle):
Total combined area: 65.27

📊 Sorting shapes by area (ascending):
Triangle(3, 4, 5): 6.00
Rectangle(5, 3): 15.00
Square(4): 16.00
Ellipse(4, 2): 25.13
Circle(4): 50.27

Concepts: Abstract classes, inheritance, polymorphism, dataclasses, magic methods, collections
'''