'''
class Cat:

    def __init__(self):
        print("A Cat has been created.")
cat1 = Cat()
cat2 = Cat()
# 1. Cat (has no attributes stored, but you can print a simple label)
print("Cats created: cat1 and cat2")


class Dog:

    def __init__(self, name):
        self.name = name
dog1 = Dog("Milo")
dog2 = Dog("Luna")
# 2. Dog (has .name)
print(f"Dog 1: {dog1.name}")
print(f"Dog 2: {dog2.name}")


class Student:

    def __init__(self, name, age):
        self.name = name
        self.age = age
student1 = Student("Aisha", 20)
student2 = Student("Ibrahim", 18)
# 3. Student (has .name and .age)
print(f"Student 1: {student1.name}, Age: {student1.age}")
print(f"Student 2: {student2.name}, Age: {student2.age}")


class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
account1 = BankAccount("Fatimah", 500)
account2 = BankAccount("Umar", 1200)
# 4. BankAccount (has .owner and .balance)
print(f"Account 1: {account1.owner} has ${account1.balance}")
print(f"Account 2: {account2.owner} has ${account2.balance}")


class Document:

    def __init__(self, title, pages):
        self.title = title
        self.pages = pages
document1 = Document("Python Basics", 250)
document2 = Document("Algorithms", 500)
# 5. Document (has .title and .pages)
print(f"Document 1: {document1.title} ({document1.pages} pages)")
print(f"Document 2: {document2.title} ({document2.pages} pages)")


class Book:
    def __init__(self, title):
        self.title = title
        self.pages_read = 0
    
    def read_pages(self, pages):
        self.pages_read += pages
        return f"Read {pages} pages. Total: {self.pages_read}"
book1 = Book("Python 101")
book2 = Book("Data Science")
# 6. Book (has .title and a method .read_pages())
print(f"Book 1: {book1.title} (Pages read: {book1.pages_read})")
print(book1.read_pages(50))  # Calling the method prints the update message!


class Friend:
    def __init__(self, name):
        self.name = name

friend1 = Friend("Amina")
friend2 = Friend("Yusuf")
friend3 = Friend("Khadijah")
# 7. Friend (has .name)
print(f"Friend 1: {friend1.name}")
print(f"Friend 2: {friend2.name}")
print(f"Friend 3: {friend3.name}")


class Cats:

    def meow(self):
        print("Meow!")
cats = Cats()
# 8. Cats (has no dots)
cats.meow()

'''
'''
for count in range(3):
    print("Grind " + str(count))

weight = 0.0
while weight < 1.5:
    weight = weight + 0.5
    print("Current weight: " + str(weight))

'''

'''
# Function with default parameter
def brew_latte(milk_type="whole", size="medium",):
    """Brew a latte with given milk type and size."""
    print(f"Brewing a {size} latte with {milk_type} milk.")

# Calls
brew_latte()  # Uses defaults: whole, medium
brew_latte("soy")  # Overrides milk_type
brew_latte(size="large", milk_type="almond")  # Keyword arguments
'''
'''
triple = lambda pir: pir == 3 and pir + 7 #and pir // pir
print(triple(5))


print(triple(6))

print(triple(23))

'''
'''
greet = lambda name: "Hello, " + name
print(greet("Bob"))
'''
'''
check_size = lambda ounces: "large" if ounces >= 16 else "small"
print(check_size(12))
print(check_size(16))
'''
'''
def wash_mugs(stack_size):
    if stack_size <= 0:  # Base case catches zero and negative safety boundaries
        print("Stack is empty!")
        return
        
    print(f"Washing mug {stack_size}")
    wash_mugs(stack_size - 1)  # Safely approaches the base case

wash_mugs(67)
'''
'''
def count_down(cups):
    if cups <= 0:
        print("Done!")
        return
    print("Cup: " + str(cups))
    count_down(cups - 1)

count_down(3)
'''
'''
menu = {
    "Latte": 4.50,
    "Espresso": 3.50
}

# Look up the price of a Latte
latte_price = menu["Latte"]
print(latte_price) # Output: 4.5

kiosk = {"status": "OFF"}
kiosk["status"] = "ON"      # Update existing
kiosk["operator"] = "Robot" # Add new
kiosk["Open"] = "sad"
print(kiosk)
'''
'''
def collect_until_stop(items):
    count = -1
    for item in items:
        count += 1
        if item.strip().lower() == "stop":
            break
    expected = items[:count]
                  
    return expected

print(collect_until_stop(["red","blue"," stop ","green"]))
print(collect_until_stop(["stop","red"]))
print(collect_until_stop(["purple","red","blue"," STop ","green"]))
'''
'''
def steam_milk():
    temp = 65
    print(f"Milk steamed to {temp} degrees.")
    return temp  # Hand the value back before the napkin is destroyed!

# Capture the returned value in a global variable
final_temp = steam_milk() + 75
print(f"The final temperature was {final_temp}")
'''
'''
# Global variable (written on the public whiteboard)
menu_price = 4.50

def serve_customer(name):
    # We can read the global variable naturally
    print(f"Charging {name} ₦{menu_price + 50:.2f} for their latte.")

serve_customer("Alice")
'''
'''
menu_price = 4.50  # Global

def show_price():
    # Reading is completely safe and permitted
    print(f"The whiteboard price is: ₦{menu_price:.2f}")

show_price()
'''
'''
total_sales = 0.0  # Global

def record_sale(amount):
    global total_sales  # Explicitly link to the global variable
    total_sales = total_sales + amount
    print(f"Sale recorded: ₦{amount:.2f}")

record_sale(4.50)
print(f"Register total sales: ₦{total_sales - 4:.2f}")
'''
'''

# A clean, single-expression calculator
calc_total = lambda price, tax: price * (1 + tax)
print(calc_total(4.50, 0.08))  # Outputs: 4.86


saw = lambda boy, girl: boy + (10 * girl)
print(saw(65, 70))

have = lambda tira: 10 * tira
print(have(65))
'''
'''
menu_prices = [4.50, 3.50, 5.00]

# Apply the ₦0.50 tax lambda to every price in the list
updated_prices = list(map(lambda price: price + 0.50, menu_prices))
updated_prices2 = [menu + 1.50
                  for menu in menu_prices]
print(updated_prices)
print(updated_prices2)
'''
'''
drinks = ["latte", "espresso", "mocha"]
loud_drinks = list(map(lambda d: d.upper(), drinks))
print(loud_drinks)
'''
'''
menu_items = [
      {"name": "Espresso", "price": 3.50},
      {"name": "Latte", "price": 4.50},
      {"name": "Mocha", "price": 5.00}
    ]

#Code to Run

# Strain out any item with a price greater than 4.50
filtered_menu = list(filter(lambda item: item["price"] == 4.50, menu_items))

print(filtered_menu)

'''
'''
menu_items = [
    {"name": "Mocha", "price": 5.00},
    {"name": "Espresso", "price": 3.50},
    {"name": "Latte", "price": 4.50}
]

# Sort the items based on their price dictionary key
sorted_by_price = sorted(menu_items, key=lambda item: item["price"])
print(sorted_by_price)
'''
'''
def wash_mugs(stack_size):
    # 1. BASE CASE (The Stop Switch)
    if stack_size == 0:
        print("All mugs are washed! Drying hands.")
        return  # Stop the function completely
        
    # 2. RECURSIVE CASE (Action + Shrink)
    print(f"Washing mug number {stack_size}...")
    
    # Call ourselves with one less mug!
    wash_mugs(stack_size - 1)

wash_mugs(3)
'''
'''
stack_size = 3
total_water_ml = 0



def calculate_water(mugs):
    if mugs <= 0:
        return 0  # Base case: 0 mugs require 0 ml
        
    # Recursive Case: 10ml for the current mug + water for the rest of the stack
    return 7 + calculate_water(mugs - 1)

total_water_ml = calculate_water(stack_size)

print(total_water_ml)

'''
'''
class KioskMachine:
    pass

print(KioskMachine)

'''
'''
class CoffeeCup:
    pass

# Stamp out two separate cup instances from the blueprint
cup_1 = CoffeeCup()
cup_2 = CoffeeCup()

print(type(cup_2)) # Output: <class '__main__.CoffeeCup'>

'''
'''
class CoffeeCup:
    # The constructor runs automatically when a cup is stamped out
    def __init__(self, size, owner):
        # self.attribute = parameter
        self.size = size          # Write the size on this specific cup
        self.owner = owner        # Write the owner on this specific cup
        self.contents = "empty"   # Default starting state for all cups

alice_cup = CoffeeCup("Large", "Alice")

print(alice_cup.size)
'''
'''

class Cup:
    def greet(self):
        print("Ready for coffee!")

my_cup = Cup()
my_cup.greet()

'''
'''
class CardboardCup:
    def __init__(self, size):
        self.size = size
        self.is_steamed = False
        
    # An instance method that operates on the cup
    def steam_cup(self):
        self.is_steamed = True
        print(f"The {self.size} cup is now steamed and warm.")

alice_cup = CardboardCup("Large")

alice_cup.steam_cup()
'''
'''
class Cup:
    def check_self(self):
        print(self)

my_cup = Cup()
print(my_cup)
my_cup.check_self()
'''
'''
class CardboardCup:
    def __init__(self, capacity):
        self.capacity_ounces = capacity
        self.contents_ounces = 0.0
        
    def fill(self, ounces):
        # Modify the attribute in-place using addition assignment
        self.contents_ounces += ounces
        print(f"Filled cup with {ounces} ounces of coffee.")

my_cup = CardboardCup(12.0)
my_cup.fill(8.0)
print(my_cup.capacity_ounces)
print(my_cup.contents_ounces)
'''
'''
class CardboardCup:
    def __init__(self, capacity):
        self.capacity_ounces = capacity
        self.contents_ounces = 0.0
        
    def fill(self, ounces):
        # Safety Gate: check if pouring would cause an overflow
        for c in range(self.capacity_ounces):
            if self.contents_ounces + ounces > self.capacity_ounces:
                print("Action Blocked: Spill Warning! This will overflow.")
            else:
                self.contents_ounces += ounces
                print(f"Successfully filled cup. Current level: {self.contents_ounces} oz")

my_cup = CardboardCup(10)
my_cup.fill(7)
'''
'''
# The Parent Class
class CardboardCup:
    def __init__(self, size):
        self.size = size
        self.is_clean = True
        self.contents_ounces = 0.0

# The Child Class (inherits everything from CardboardCup)
class InsulatedCup(CardboardCup):
    # We do not write any code here yet
    pass

# We can instantiate the child class using the parent's constructor!
premium_cup = InsulatedCup("large")
print(premium_cup.size)     # Output: large (Inherited!)
print(premium_cup.is_clean) # Output: True  (Inherited!)
'''
'''
class Cup:
    def greet(self):
        print("Hello from Parent")

class KidCup(Cup):
    pass

k = KidCup()
k.greet()
'''
'''
class CardboardCup:
    def get_material(self):
        return "paper"

class InsulatedCup(CardboardCup):
    # Override the parent method completely
    def get_material(self):
        return "double-walled paper"

standard = CardboardCup()
premium = InsulatedCup()

print(standard.get_material()) # Output: paper
print(premium.get_material())  # Output: double-walled paper
'''
'''
class Cup:
    def show(self):
        print("Standard Cup")

class CustomCup(Cup):
    def show(self):
        print("Custom Cup!")

c = CustomCup()
c.show()
'''
'''
class CardboardCup:
    def __init__(self):
        self.contents_ounces = 3.0
        
    def fill(self, ounces):
        self.contents_ounces += ounces

class InsulatedCup(CardboardCup):
    def __init__(self):
        # Run the parent's constructor first!
        super().__init__()
        self.has_temp_check = True
        
    def fill(self, ounces):
        # 1. Use super() to run the base pouring math
        super().fill(ounces)
        # 2. Perform specialized child actions
        print("Insulation layer activated. Heat is trapped.")

premium_cup = InsulatedCup()
premium_cup.fill(8.0)
'''
'''
class Cup:
    def fill(self):
        print("Pouring...")

class SuperCup(Cup):
    def fill(self):
        super().fill()
        print("Locking lid!")

sc = SuperCup()
sc.fill()
'''
'''
class CardboardCup:
    def __init__(self, size, drink):
        self.size = size
        self.drink = drink
        
    # The __str__ method MUST return a string
    def __str__(self):
        return f"{self.size.capitalize()} {self.drink} Cup"

alice_cup = CardboardCup("large", "Latte")
print(alice_cup) # Output: Large Latte Cup
'''
'''
class Cup:
    def __str__(self):
        return "A clean cup"

print(Cup())
'''
'''
class CardboardCup:
    def __init__(self, size, drink):
        self.size = size
        self.drink = drink
        
    def __repr__(self):
        # Format the output to look like the instantiation call
        return f"CardboardCup('{self.size}', '{self.drink}')"

cup_list = [CardboardCup("small", "Espresso"), CardboardCup("large", "Latte")]
print(cup_list) # Output: [CardboardCup('small', 'Espresso'), CardboardCup('large', 'Latte')]
'''
'''
class Cup:
    def __repr__(self):
        return "Cup()"

print([Cup(), Cup()])
'''
'''
class CardboardCup:
    def __init__(self, owner):
        self.owner = owner

class CupStack:
    def __init__(self):
        # The internal list used to hold our cups
        self._cups = []
        
    def push(self, cup):
        self._cups.append(cup)  # Push to the top of the stack
        
    def pop(self):
        # Safety check: do not pop if the stack is empty!
        if self.is_empty():
            print("Action Blocked: The stack is empty!")
            return None
        return self._cups.pop()  # Pop from the top of the stack
        
    def is_empty(self):
        return len(self._cups) == 0

stack = []
stack.append("Cup A") # Push
stack.append("Cup B") # Push
print(stack.pop())    # Pop (LIFO)
'''
'''
class CupQueue:
    def __init__(self):
        self._cups = []
        
    def enqueue(self, cup):
        self._cups.append(cup)  # Add to the back of the line
        
    def dequeue(self):
        if self.is_empty():
            print("Action Blocked: The conveyor chute is empty!")
            return None
        return self._cups.pop(0)  # Remove from the front of the line (Index 0)
        
    def is_empty(self):
        return len(self._cups) == 0

stack = []
stack.append("Cup A") # Push
stack.append("Cup B") # Push
print(stack.pop())    # Pop (LIFO)
'''
'''
class CupQueue:
    def __init__(self):
        self._cups = []
    def dequeue(self):
        return self._cups.pop(0)  # Index 0 is always the oldest item
queue = ["Cup A", "Cup B"]
print(queue.pop(0)) # Dequeue
print(queue)
'''
'''
class CupNode:
    def __init__(self, name):
        self.customer_name = name  # The data stored in the link
        self.next = None           # Pointer to the next cup (defaults to empty)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

node_1 = Node("Alice")
print(node_1.data)
print(node_1.next)

# 1. Create three separate cup nodes
cup_1 = CupNode("Alice")
cup_2 = CupNode("Bob")
cup_3 = CupNode("Charlie")

# 2. Tie the strings!
cup_1.next = cup_2  # Alice points to Bob
cup_2.next = cup_3  # Bob points to Charlie
# cup_3.next remains None (the end of the line)

# 3. Read the linked chain using nested dot notation
print(cup_1.next.customer_name)       # Output: Bob
print(cup_1.next.next.customer_name)  # Output: Charlie
'''
'''
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

n1 = Node("A")
n2 = Node("B")
n1.next = n2

print(n1.next.val)
'''

'''
class CoffeeMachine:

    def make_coffee(self):
        print("Grinding beans...")
        print("Heating water...")
        print("Filtering coffee...")
        print("Coffee ready!")

machine = CoffeeMachine()
machine.make_coffee()
'''
'''
class Classroom:

    def __init__(self):
        self.students = []

classroom = Classroom()

len(classroom)
'''
'''
class Classroom:
    def __init__(self):
        self.students = [2, 3, 5, 5, 7]

    def __len__(self):
        return len(self.students)

classroom = Classroom()
print(len(classroom))
'''
'''
class Student:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __len__(self):
        return len(self.name)

student = Student("Amina")

print(student)
print(len(student))


class Book:

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"

    def __len__(self):
        return len(f"{self.title} and {self.author}")

book = Book("Python 101", "John")
print(book)
print(len(book))

'''
'''
class Book:

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Book('{self.title}')"

book = Book("Python 101")
print(book)
'''
'''
class Student:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

student1 = Student("Amina")
student2 = Student("Amina")

print(student1 == student2)

'''
'''
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Money(self.amount + other.amount)

    def __str__(self):
        return f"${self.amount}"

money1 = Money(5)
money2 = Money(3)
money3 = money1 + money2
print(money3)
'''
'''
numbers = [10, 20, 30]
iterator = iter(numbers)
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))
'''
'''
class CountToThree:

    def __init__(self):
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.number <= 3:
            current = self.number
            self.number += 1
            return current

        raise StopIteration

counter = CountToThree()
print(next(counter))
print(next(counter))
print(next(counter))
print(next(counter))

counter = CountToThree()

for number in counter:
    print(number)

'''
'''
class RangeThrough:
    def __init__(self, passed):
        self.number = 0
        self.passed = passed

    def __iter__(self):
        return self

    def __next__(self):
        if self.number <= self.passed:
            current = self.number
            self.number += 1
            return current
        raise StopIteration

r = RangeThrough(5)
for number in r:
    print(number)

'''
'''
def demo():
    print("A")
    yield 10
    print("B")
    yield 20
    print("C")
    yield 30

g = demo()

print(next(g))
print(next(g))


def get_numbers():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5



f = get_numbers()
d = list(f)
print(d)

'''
'''
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def __str__(self):
        values = []
        current = self.head
        while current is not None:
            values.append(str(current.data))
            current = current.next
        return " -> ".join(values)

numbers = LinkedList()

numbers.append(10)
numbers.append(20)
numbers.append(30)
numbers.append(40)

print(numbers)
'''

'''
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def display(self):
        current = self.head

        while current is not None:
            print(current.data)
            current = current.next

numbers = LinkedList()

numbers.append(10)
numbers.append(20)
numbers.append(30)

numbers.display()
'''