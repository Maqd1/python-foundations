from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


# ============================================================
# VALUE OBJECTS
# ============================================================

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "NGN"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative.")

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError("Currencies must match.")

        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError("Currencies must match.")

        result = self.amount - other.amount

        if result < 0:
            result = 0

        return Money(result, self.currency)

    def __mul__(self, quantity):
        if not isinstance(quantity, (int, float)):
            return NotImplemented

        return Money(self.amount * quantity, self.currency)

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        return self.amount < other.amount

    def __le__(self, other):
        if not isinstance(other, Money):
            return NotImplemented

        return self.amount <= other.amount

    def __str__(self):
        return f"₦{self.amount:,.2f}"


@dataclass(frozen=True)
class Address:
    name: str
    city: str
    state: str = ""

    def __str__(self):
        if self.state:
            return f"{self.name}, {self.city}, {self.state}"

        return f"{self.name}, {self.city}"


# ============================================================
# PRODUCT HIERARCHY
# ============================================================

@dataclass
class Product(ABC):
    id: str
    name: str
    price: Money
    category: str
    stock: int

    def __post_init__(self):
        if self.stock < 0:
            raise ValueError("Stock cannot be negative.")

        if self.price.amount < 0:
            raise ValueError("Price cannot be negative.")

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if not isinstance(value, int):
            raise TypeError("Stock must be an integer.")

        if value < 0:
            raise ValueError("Stock cannot be negative.")

        self._stock = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, Money):
            raise TypeError("Price must be a Money object.")

        if value.amount < 0:
            raise ValueError("Price cannot be negative.")

        self._price = value

    def reduce_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if quantity > self.stock:
            raise ValueError(
                f"Not enough stock for {self.name}."
            )

        self.stock -= quantity

    def increase_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.stock += quantity

    def __eq__(self, other):
        if not isinstance(other, Product):
            return NotImplemented

        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.name} ({self.category})"


@dataclass
class Electronics(Product):
    warranty_period: int = 0

    def __post_init__(self):
        super().__post_init__()

        if self.warranty_period < 0:
            raise ValueError(
                "Warranty period cannot be negative."
            )


@dataclass
class Clothing(Product):
    size: str = ""
    material: str = ""


@dataclass
class Food(Product):
    expiration_date: date = field(
        default_factory=date.today
    )
    weight: float = 0

    def __post_init__(self):
        super().__post_init__()

        if self.weight <= 0:
            raise ValueError(
                "Food weight must be greater than zero."
            )


# ============================================================
# CART ITEMS
# ============================================================

@dataclass
class CartItem:
    product: Product
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError(
                "Cart quantity must be greater than zero."
            )

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return (
            f"{self.product.name} "
            f"x {self.quantity}"
        )


# ============================================================
# DISCOUNT STRATEGY
# ============================================================

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, cart):
        """Return the discount amount."""
        pass

    @abstractmethod
    def description(self):
        pass


@dataclass
class PercentageDiscount(DiscountStrategy):
    percentage: float
    code: str

    def __post_init__(self):
        if not 0 <= self.percentage <= 100:
            raise ValueError(
                "Percentage must be between 0 and 100."
            )

    def apply(self, cart):
        return cart.subtotal * (self.percentage / 100)

    def description(self):
        return f"{self.percentage:g}% off ({self.code})"


@dataclass
class FixedDiscount(DiscountStrategy):
    amount: Money
    code: str

    def apply(self, cart):
        return min(
            self.amount.amount,
            cart.subtotal
        )

    def description(self):
        return f"{self.amount} off ({self.code})"


@dataclass
class BuyXGetYFree(DiscountStrategy):
    product_id: str
    buy_quantity: int
    free_quantity: int
    code: str

    def __post_init__(self):
        if self.buy_quantity <= 0:
            raise ValueError(
                "Buy quantity must be greater than zero."
            )

        if self.free_quantity <= 0:
            raise ValueError(
                "Free quantity must be greater than zero."
            )

    def apply(self, cart):
        discount = 0

        for item in cart.items:
            if item.product.id != self.product_id:
                continue

            groups = item.quantity // (
                self.buy_quantity + self.free_quantity
            )

            remaining = item.quantity % (
                self.buy_quantity + self.free_quantity
            )

            free_items = groups * self.free_quantity

            if remaining >= self.buy_quantity:
                free_items += self.free_quantity

            discount += (
                item.product.price.amount
                * free_items
            )

        return discount

    def description(self):
        return (
            f"Buy {self.buy_quantity} "
            f"Get {self.free_quantity} Free "
            f"({self.code})"
        )


@dataclass
class CategoryDiscount(DiscountStrategy):
    category: str
    percentage: float
    code: str

    def __post_init__(self):
        if not 0 <= self.percentage <= 100:
            raise ValueError(
                "Percentage must be between 0 and 100."
            )

    def apply(self, cart):
        category_total = sum(
            item.subtotal.amount
            for item in cart.items
            if item.product.category.lower()
            == self.category.lower()
        )

        return category_total * (
            self.percentage / 100
        )

    def description(self):
        return (
            f"{self.percentage:g}% off "
            f"{self.category} ({self.code})"
        )


# ============================================================
# INVENTORY
# ============================================================

class Inventory:
    def __init__(self, low_stock_threshold=5):
        self.products = {}
        self.low_stock_threshold = low_stock_threshold
        self.reserved = {}

    def add_product(self, product):
        if product.id in self.products:
            raise ValueError(
                f"Product ID {product.id} already exists."
            )

        self.products[product.id] = product

    def get_product(self, product_id):
        product = self.products.get(product_id)

        if product is None:
            raise KeyError(
                f"Product {product_id} not found."
            )

        return product

    def available_stock(self, product_id):
        product = self.get_product(product_id)

        reserved = self.reserved.get(product_id, 0)

        return product.stock - reserved

    def reserve(self, product_id, quantity):
        product = self.get_product(product_id)

        if quantity <= 0:
            raise ValueError(
                "Reservation quantity must be greater than zero."
            )

        available = self.available_stock(product_id)

        if quantity > available:
            raise ValueError(
                f"Not enough available stock for "
                f"{product.name}. "
                f"Available: {available}"
            )

        self.reserved[product_id] = (
            self.reserved.get(product_id, 0)
            + quantity
        )

    def release(self, product_id, quantity):
        current = self.reserved.get(product_id, 0)

        released = min(quantity, current)

        if released == current:
            self.reserved.pop(product_id, None)
        else:
            self.reserved[product_id] = current - released

    def confirm_reservation(self, product_id, quantity):
        product = self.get_product(product_id)

        reserved = self.reserved.get(product_id, 0)

        if quantity > reserved:
            raise ValueError(
                "Cannot confirm more stock than reserved."
            )

        product.reduce_stock(quantity)

        self.release(product_id, quantity)

    def low_stock_products(self):
        return [
            product
            for product in self.products.values()
            if self.available_stock(product.id)
            <= self.low_stock_threshold
        ]

    def display_low_stock_alerts(self):
        products = self.low_stock_products()

        if not products:
            print("✅ No low-stock products.")
            return

        print("\n⚠️ LOW STOCK ALERTS")

        for product in products:
            print(
                f"- {product.name}: "
                f"{self.available_stock(product.id)} left"
            )


# ============================================================
# SHOPPING CART
# ============================================================

class ShoppingCart:
    def __init__(self, inventory):
        self.inventory = inventory
        self.items = []
        self.discounts = []
        self.coupon_codes = set()

    def add_item(self, product_id, quantity):
        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        product = self.inventory.get_product(product_id)

        existing = next(
            (
                item
                for item in self.items
                if item.product.id == product_id
            ),
            None
        )

        current_quantity = (
            existing.quantity if existing else 0
        )

        available = self.inventory.available_stock(
            product_id
        )

        if current_quantity + quantity > available:
            raise ValueError(
                f"Not enough stock. "
                f"Available: {available}"
            )

        if existing:
            existing.quantity += quantity
        else:
            self.items.append(
                CartItem(product, quantity)
            )

        print(
            f"Added: {product.name} "
            f"({quantity})"
        )

    def remove_item(self, product_id):
        for item in self.items:
            if item.product.id == product_id:
                self.items.remove(item)

                print(
                    f"Removed: {item.product.name}"
                )

                return

        raise KeyError(
            f"Product {product_id} is not in the cart."
        )

    @property
    def subtotal(self):
        return sum(
            item.subtotal.amount
            for item in self.items
        )

    def apply_discount(self, discount):
        if discount.code in self.coupon_codes:
            raise ValueError(
                "This coupon has already been applied."
            )

        discount_amount = discount.apply(self)

        if discount_amount <= 0:
            raise ValueError(
                "This discount does not apply."
            )

        self.discounts.append(discount)
        self.coupon_codes.add(discount.code)

        print(
            f"✅ Applied {discount.description()}"
        )

    @property
    def total_discount(self):
        return min(
            self.subtotal,
            sum(
                discount.apply(self)
                for discount in self.discounts
            )
        )

    @property
    def total(self):
        return max(
            0,
            self.subtotal - self.total_discount
        )

    def validate_stock(self):
        for item in self.items:
            available = self.inventory.available_stock(
                item.product.id
            )

            if item.quantity > available:
                raise ValueError(
                    f"Not enough stock for "
                    f"{item.product.name}. "
                    f"Available: {available}"
                )

        return True

    def reserve_stock(self):
        self.validate_stock()

        reserved = []

        try:
            for item in self.items:
                self.inventory.reserve(
                    item.product.id,
                    item.quantity
                )

                reserved.append(item)

        except Exception:
            for item in reserved:
                self.inventory.release(
                    item.product.id,
                    item.quantity
                )

            raise

    def clear(self):
        self.items.clear()
        self.discounts.clear()
        self.coupon_codes.clear()

    def display(self):
        print("\n🛒 SHOPPING CART")

        if not self.items:
            print("Cart is empty.")
            return

        for item in self.items:
            print(
                f"- {item.product.name} "
                f"x {item.quantity} "
                f"= {item.subtotal}"
            )

        print(
            f"\nSubtotal: "
            f"₦{self.subtotal:,.2f}"
        )

        print(
            f"Discount: "
            f"-₦{self.total_discount:,.2f}"
        )

        print(
            f"Total: "
            f"₦{self.total:,.2f}"
        )


# ============================================================
# ORDER SYSTEM
# ============================================================

class OrderStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


@dataclass
class OrderItem:
    product_name: str
    quantity: int
    unit_price: Money
    free_quantity: int = 0

    @property
    def paid_quantity(self):
        return self.quantity - self.free_quantity

    @property
    def total(self):
        return self.unit_price * self.paid_quantity


class Order:
    def __init__(
        self,
        order_id,
        items,
        subtotal,
        discount,
        total,
        shipping_address
    ):
        self.order_id = order_id
        self.items = items
        self.subtotal = subtotal
        self.discount = discount
        self.total = total
        self.shipping_address = shipping_address
        self.status = OrderStatus.PENDING

    def confirm(self):
        self.status = OrderStatus.CONFIRMED

    def update_status(self, status):
        if not isinstance(status, OrderStatus):
            raise TypeError(
                "Status must be an OrderStatus."
            )

        self.status = status

    def invoice(self):
        print("\n" + "=" * 55)
        print("📄 INVOICE")
        print("=" * 55)

        print(f"Order: {self.order_id}")
        print(f"Status: {self.status.value}")
        print(f"Shipping to: {self.shipping_address}")

        print("\nItems:")

        for item in self.items:
            free_text = ""

            if item.free_quantity:
                free_text = (
                    f" [{item.free_quantity} free]"
                )

            print(
                f"- {item.product_name} "
                f"x {item.quantity}"
                f"{free_text} "
                f"= {item.total}"
            )

        print(
            f"\nSubtotal: ₦{self.subtotal:,.2f}"
        )
        print(
            f"Discount: -₦{self.discount:,.2f}"
        )
        print(
            f"Total: ₦{self.total:,.2f}"
        )

        print("=" * 55)

    def __str__(self):
        return (
            f"Order {self.order_id} "
            f"({self.status.value})"
        )


class OrderManager:
    def __init__(self):
        self.orders = []
        self.next_order_number = 1

    def create_order(self, cart, shipping_address):
        if not cart.items:
            raise ValueError(
                "Cannot create an order from an empty cart."
            )

        cart.validate_stock()
        cart.reserve_stock()

        try:
            order_items = []

            for item in cart.items:
                free_quantity = self._calculate_free_quantity(
                    cart,
                    item
                )

                order_items.append(
                    OrderItem(
                        product_name=item.product.name,
                        quantity=item.quantity,
                        unit_price=item.product.price,
                        free_quantity=free_quantity
                    )
                )

            for item in cart.items:
                self._confirm_stock(
                    item.product.id,
                    item.quantity
                )

            order_id = (
                f"ORD-{self.next_order_number:03d}"
            )

            order = Order(
                order_id=order_id,
                items=order_items,
                subtotal=cart.subtotal,
                discount=cart.total_discount,
                total=cart.total,
                shipping_address=shipping_address
            )

            order.confirm()

            self.orders.append(order)
            self.next_order_number += 1

            cart.clear()

            return order

        except Exception:
            for item in cart.items:
                self._release_stock(
                    item.product.id,
                    item.quantity
                )

            raise

    def _calculate_free_quantity(self, cart, item):
        free_quantity = 0

        for discount in cart.discounts:
            if not isinstance(
                discount,
                BuyXGetYFree
            ):
                continue

            if discount.product_id != item.product.id:
                continue

            group_size = (
                discount.buy_quantity
                + discount.free_quantity
            )

            groups = item.quantity // group_size
            remaining = item.quantity % group_size

            free = groups * discount.free_quantity

            if remaining >= discount.buy_quantity:
                free += discount.free_quantity

            free_quantity = max(
                free_quantity,
                free
            )

        return free_quantity

    def _confirm_stock(self, product_id, quantity):
        inventory = None

        # Inventory is retrieved from the cart indirectly
        # through the current order creation context.
        # This method is replaced below by direct assignment.
        raise NotImplementedError


    def _release_stock(self, product_id, quantity):
        raise NotImplementedError


# ============================================================
# FIX ORDER MANAGER INVENTORY CONNECTION
# ============================================================

class OrderManagerWithInventory(OrderManager):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory

    def _confirm_stock(self, product_id, quantity):
        self.inventory.confirm_reservation(
            product_id,
            quantity
        )

    def _release_stock(self, product_id, quantity):
        self.inventory.release(
            product_id,
            quantity
        )


# ============================================================
# DISPLAY HELPERS
# ============================================================

def display_products(inventory):
    print("\n📦 PRODUCTS:")

    for number, product in enumerate(
        inventory.products.values(),
        start=1
    ):
        print(
            f"\n{number}. "
            f"{product.name} "
            f"({product.category}) "
            f"- {product.price}"
        )

        if isinstance(product, Electronics):
            print(
                f"   Warranty: "
                f"{product.warranty_period} months"
            )

        elif isinstance(product, Clothing):
            print(
                f"   Size: {product.size}, "
                f"Material: {product.material}"
            )

        elif isinstance(product, Food):
            print(
                f"   Weight: {product.weight:g}g, "
                f"Expires: "
                f"{product.expiration_date}"
            )

        print(
            f"   Stock: "
            f"{inventory.available_stock(product.id)}"
        )


def display_checkout(cart):
    print("\n📋 CHECKOUT")

    for item in cart.items:
        free_quantity = 0

        for discount in cart.discounts:
            if isinstance(
                discount,
                BuyXGetYFree
            ):
                if discount.product_id == item.product.id:
                    group_size = (
                        discount.buy_quantity
                        + discount.free_quantity
                    )

                    groups = (
                        item.quantity // group_size
                    )

                    remaining = (
                        item.quantity % group_size
                    )

                    free_quantity = max(
                        free_quantity,
                        groups * discount.free_quantity
                    )

                    if remaining >= discount.buy_quantity:
                        free_quantity += (
                            discount.free_quantity
                        )

        paid_quantity = (
            item.quantity - free_quantity
        )

        print(
            f"{paid_quantity}x "
            f"{item.product.name} @ "
            f"{item.product.price} = "
            f"₦{item.product.price.amount * paid_quantity:,.2f}"
        )

        if free_quantity:
            print(
                f"   {free_quantity}x "
                f"{item.product.name} (free)"
            )

    print(
        f"\nSubtotal: "
        f"₦{cart.subtotal:,.2f}"
    )

    print(
        f"Discount: "
        f"-₦{cart.total_discount:,.2f}"
    )

    print(
        f"Total: "
        f"₦{cart.total:,.2f}"
    )


# ============================================================
# DEMONSTRATION
# ============================================================

def main():
    inventory = Inventory(
        low_stock_threshold=5
    )

    laptop = Electronics(
        id="P001",
        name="Laptop",
        price=Money(450000),
        category="Electronics",
        stock=10,
        warranty_period=24
    )

    tshirt = Clothing(
        id="P002",
        name="T-Shirt",
        price=Money(15000),
        category="Clothing",
        stock=25,
        size="L",
        material="Cotton"
    )

    chocolate = Food(
        id="P003",
        name="Chocolate",
        price=Money(1500),
        category="Food",
        stock=50,
        expiration_date=date(2026, 12, 31),
        weight=200
    )

    inventory.add_product(laptop)
    inventory.add_product(tshirt)
    inventory.add_product(chocolate)

    print("\n🛒 E-COMMERCE SYSTEM 🛒")

    display_products(inventory)

    # --------------------------------------------------------
    # CART
    # --------------------------------------------------------

    cart = ShoppingCart(inventory)

    print("\n🛒 SHOPPING CART")

    cart.add_item("P001", 2)
    cart.add_item("P002", 3)
    cart.add_item("P003", 5)

    print(
        f"\nCart Total: "
        f"₦{cart.subtotal:,.2f}"
    )

    # --------------------------------------------------------
    # DISCOUNTS
    # --------------------------------------------------------

    discounts = {
        "SAVE10": PercentageDiscount(
            percentage=10,
            code="SAVE10"
        ),

        "SAVE5K": FixedDiscount(
            amount=Money(5000),
            code="SAVE5K"
        ),

        "BOGO": BuyXGetYFree(
            product_id="P002",
            buy_quantity=2,
            free_quantity=1,
            code="BOGO"
        ),

        "FOOD10": CategoryDiscount(
            category="Food",
            percentage=10,
            code="FOOD10"
        )
    }

    print("\nAvailable Discounts:")

    for discount in discounts.values():
        print(
            f"- {discount.description()}"
        )

    print("\nApply discount: SAVE10")

    cart.apply_discount(
        discounts["SAVE10"]
    )

    print(
        f"\nNew Total: "
        f"₦{cart.total:,.2f}"
    )

    print("\nApply additional discount? (y/n): y")
    print("Apply discount: BOGO")

    cart.apply_discount(
        discounts["BOGO"]
    )

    print(
        f"\nNew Total: "
        f"₦{cart.total:,.2f}"
    )

    # --------------------------------------------------------
    # CHECKOUT
    # --------------------------------------------------------

    display_checkout(cart)

    address = Address(
        name="Damilola",
        city="Lagos"
    )

    print(
        f"\nShipping to: {address}"
    )

    print(
        "Estimated delivery: 3-5 days"
    )

    print("\nConfirm order? (y/n): y")

    order_manager = OrderManagerWithInventory(
        inventory
    )

    order = order_manager.create_order(
        cart,
        address
    )

    print(
        f"\n✅ Order placed! "
        f"Order #{order.order_id}"
    )

    print("\n📊 ORDER DETAILS")
    print(f"Order #{order.order_id}")
    print(f"Status: {order.status.value}")
    print(
        f"Total: "
        f"₦{order.total:,.2f}"
    )

    print("\nItems:")

    for item in order.items:
        free_text = ""

        if item.free_quantity:
            free_text = (
                f" [{item.free_quantity} free]"
            )

        print(
            f"- {item.product_name} "
            f"({item.quantity})"
            f"{free_text}"
        )

    print(
        f"\nShipping to: "
        f"{order.shipping_address}"
    )

    print(
        "Estimated delivery: 3-5 days"
    )

    # --------------------------------------------------------
    # INVOICE
    # --------------------------------------------------------

    order.invoice()

    # --------------------------------------------------------
    # INVENTORY
    # --------------------------------------------------------

    print("\n📦 INVENTORY AFTER ORDER")

    display_products(inventory)

    inventory.display_low_stock_alerts()


if __name__ == "__main__":
    main()