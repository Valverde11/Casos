from abc import ABC, abstractmethod

# --- Component ---
class Sandwich(ABC):
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def price(self):
        pass


# --- Concrete Component ---
class BaseSandwich(Sandwich):
    def __init__(self, protein: str, size_cm: int):
        self.protein = protein
        self.size_cm = size_cm

        prices = {
            "Pavo": {15: 12.0, 30: 18.0},
            "Italiano": {15: 9.0, 30: 16.0},
            "Beef": {15: 10.0, 30: 16.0},
            "Veggie": {15: 8.0, 30: 14.0},
            "Atún": {15: 11.0, 30: 17.0},
            "Pollo": {15: 12.0, 30: 18.0},
        }

        self._price = prices[protein][size_cm]

    def description(self):
        return f"{self.protein} ({self.size_cm} cm)"

    def price(self):
        return self._price


# --- Decorator ---
class SandwichDecorator(Sandwich):
    def __init__(self, sandwich: Sandwich):
        self.sandwich = sandwich
        self.size_cm = sandwich.size_cm  # NECESARIO

    def description(self):
        return self.sandwich.description()

    def price(self):
        return self.sandwich.price()


# -------- ADICIONALES -------- #

class Aguacate(SandwichDecorator):
    def description(self):
        return f"{self.sandwich.description()} + Aguacate"

    def price(self):
        return self.sandwich.price() + (1.5 if self.size_cm == 15 else 2.5)


class DobleProteina(SandwichDecorator):
    def description(self):
        return f"{self.sandwich.description()} + Doble Proteína"

    def price(self):
        return self.sandwich.price() + (4.5 if self.size_cm == 15 else 8)


class Hongos(SandwichDecorator):
    def description(self):
        return f"{self.sandwich.description()} + Hongos"

    def price(self):
        return self.sandwich.price() + (0.85 if self.size_cm == 15 else 1.45)


class Refresco(SandwichDecorator):
    def description(self):
        return f"{self.sandwich.description()} + Refresco"

    def price(self):
        return self.sandwich.price() + 1.0


class Sopa(SandwichDecorator):
    def description(self):
        return f"{self.sandwich.description()} + Sopa"

    def price(self):
        return self.sandwich.price() + 4.2


class Postre(SandwichDecorator):
    def description(self):
        return f"{self.sandwich.description()} + Postre"

    def price(self):
        return self.sandwich.price() + 3.5


# Lista para uso de gui.py
ADICIONALES = {
    "Aguacate": Aguacate,
    "Doble Proteína": DobleProteina,
    "Hongos": Hongos,
    "Refresco": Refresco,
    "Sopa": Sopa,
    "Postre": Postre
}
