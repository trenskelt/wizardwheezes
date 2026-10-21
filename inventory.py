# Trent Skelton, 2026-10-21
# Weasleys' Wizard Wheezes inventory tracker
from datetime import datetime

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class Product:
    """
    One joke product sold in the shop.
    Attributes:
    name (str): Product name.
    price (float): Price in Galleons.
    daily_sales (list): Units sold each day, in DAYS order.
    """

    def __init__(self, name, price):
        """Create a product with no sales recorded yet."""
        self.name = name
        self.price = price
        self.daily_sales = []

    def total_units(self):
        """Return total units sold across all days (int)."""
        return sum(self.daily_sales)

    def revenue(self):
        """Return total Galleons earned by this product (float)."""
        return self.total_units() * self.price

    def best_day(self):
        """Return the DAYS name on which this product sold the most (str)."""
        best_index = self.daily_sales.index(max(self.daily_sales))
        return DAYS[best_index]

    def report_line(self):
        """Return a one-line summary for the sales report (str)."""
        return f"{self.name}: {self.total_units()} units, {self.revenue():.2f} Galleons"


def get_int(prompt, low, high):
    """Ask until the user enters a whole number in the given range.

    Parameters:
    prompt (str): Text to show.
    low (int): Smallest allowed value.
    high (int): Largest allowed value.
    Returns:
    int: The validated number.
    """
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f" Enter a number from {low} to {high}.")
        except ValueError:
            print(" Whole numbers only.")


def get_float(prompt):
    """Ask until the user types a price greater than zero (float)."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print(" Price must be more than zero.")
        except ValueError:
            print(" Enter a number such as 3.50.")


def build_inventory():
    """
    Ask how many products the shop stocks, then collect each one's
    name, price, and seven days of sales.
    Returns:
    list: Product objects with daily_sales filled in.
    """
    count = get_int("How many products are on the shelves? ", 1, 50)
    inventory = []
    while len(inventory) < count:
        name = input(f"Product {len(inventory) + 1} name: ").strip()
        if not name:
            print(" Name cannot be blank.")
            continue

        price = get_float(f"Price of {name} in Galleons: ")
        product = Product(name, price)
        for day in DAYS:
            product.daily_sales.append(get_int(f" {day} units sold: ", 0, 500))
        inventory.append(product)

    print(f"\nStocked {count} product(s).\n")
    return inventory
def rank_by_revenue(inventory):
    """
    Order products from highest revenue to lowest.
    Parameters:
    inventory (list): Product objects.
    Returns:
    list: The same objects, sorted by revenue descending.
    """
    return sorted(inventory, key=Product.revenue, reverse=True)


def busiest_day(inventory):
    """
    Find the day with the most units sold across all products.
    Parameters:
    inventory (list): Product objects with daily_sales filled in.
    Returns:
    tuple: (day_name, total_units_that_day)
    """
    all_sales = [product.daily_sales for product in inventory]
    day_totals = [sum(day) for day in zip(*all_sales)]
    best_index = day_totals.index(max(day_totals))
    return DAYS[best_index], day_totals[best_index]


def total_revenue(inventory):
    """Return the shop's combined revenue across all products (float)."""
    return sum(product.revenue() for product in inventory)

def save_report(ranked, filename="daily_report.txt"):
    """
    Write the sales report to a text file.
    Parameters:
    ranked (list): Product objects sorted by revenue.
    filename (str): Output file name.
    """
    day, units = busiest_day(ranked)
    lines = [
        "Weasleys' Wizard Wheezes Daily Report",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
        f"Products: {len(ranked)}",
        "",
        "Ranked by revenue:",
        *(product.report_line() for product in ranked),
        "",
        f"Busiest day: {day} ({units} units)",
        f"Total revenue: {total_revenue(ranked):.2f} Galleons",
    ]
    try:
        with open(filename, "w", encoding="utf-8") as report:
            report.write("\n".join(lines) + "\n")
        print(f"Report saved to {filename}")
    except OSError as error:
        print(f"Could not save report: {error}")
def main():
    """Run the inventory program from start to finish."""
    print("Weasleys' Wizard Wheezes Daily Inventory\n")
    inventory = build_inventory()
    ranked = rank_by_revenue(inventory)

    for product in ranked:
        print(product.report_line())
    day, units = busiest_day(ranked)
    print(f"\nBusiest day: {day} ({units} units)")
    print(f"Total revenue: {total_revenue(ranked):.2f} Galleons")
    save_report(ranked)
if __name__ == "__main__":
    main()
