# models.py
import random
from dataclasses import dataclass
from typing import List, Callable, Optional

@dataclass
class Attack:
    name: str
    min_power: int
    max_power: int
    special: Optional[str] = None  # None, "heal", "extra"

    def roll(self) -> int:
        return random.randint(self.min_power, self.max_power)

    def execute(self, attacker: "Player", defender: "Player", log: Callable[[str], None]):
        power = self.roll()
        if self.special is None:
            defender.life -= power
            log(f"{attacker.name} usa {self.name} causando {power} de daño. ({defender.name} vida={max(defender.life,0)})")
        elif self.special == "heal":
            attacker.life += power
            log(f"{attacker.name} usa {self.name} y se CURA {power}. ({attacker.name} vida={attacker.life})")
        elif self.special == "extra":
            extra = 10
            defender.life -= (power + extra)
            log(f"{attacker.name} usa {self.name} causando {power}+{extra} de daño (extra). ({defender.name} vida={max(defender.life,0)})")

        # clamp
        if defender.life < 0:
            defender.life = 0

@dataclass
class MartialArt:
    name: str
    attacks: List[Attack]
    description: str = ""

    def perform_hits(self, attacker: "Player", defender: "Player", hits: int, log: Callable[[str], None]):
        """Execute 'hits' attacks randomly chosen from this martial art's attacks."""
        log(f"{attacker.name} usa la técnica '{self.name}' ({hits} golpes)")
        for i in range(hits):
            attack = random.choice(self.attacks)
            attack.execute(attacker, defender, log)
            if defender.life <= 0:
                log(f"{defender.name} quedó en 0 vida.")
                break

class Player:
    def __init__(self, name: str):
        self.name = name
        self.life: int = 200
        self.arts: List[MartialArt] = []
        self.battle_log: List[str] = []

    def assign_random_arts(self, pool: List[MartialArt], k: int = 3):
        self.arts = random.sample(pool, k)

    def is_alive(self) -> bool:
        return self.life > 0

    def add_log(self, text: str):
        self.battle_log.append(text)

# ------------------------------------------------------------------
# Pool: 10 artes marciales, cada golpe entre 5 y 50
# ------------------------------------------------------------------
def create_arts_pool() -> List[MartialArt]:
    pool: List[MartialArt] = []

    pool.append(MartialArt("Karate", [
        Attack("Gyaku-zuki", 10, 25),
        Attack("Mawashi-geri", 15, 40),
        Attack("Kiai Heal", 5, 20, special="heal")
    ], "Balanceado"))

    pool.append(MartialArt("Taekwondo", [
        Attack("Dollyo Chagi", 12, 30),
        Attack("Neryo Chagi", 20, 45),
        Attack("Ap Chagi Extra", 10, 25, special="extra")
    ], "Patadas potentes"))

    pool.append(MartialArt("Kung Fu", [
        Attack("Palm Strike", 12, 32),
        Attack("Tiger Claw", 18, 40),
        Attack("Chi Heal", 5, 20, special="heal")
    ], "Daño alto posible"))

    pool.append(MartialArt("Muay Thai", [
        Attack("Elbow Strike", 15, 35),
        Attack("Knee Strike", 20, 45),
        Attack("Clinch Extra", 10, 25, special="extra")
    ], "Rodillas y codos"))

    pool.append(MartialArt("Boxeo", [
        Attack("Jab", 5, 15),
        Attack("Cross", 15, 30),
        Attack("Uppercut", 20, 40)
    ], "Golpes rápidos"))

    pool.append(MartialArt("Judo", [
        Attack("O-goshi", 10, 25),
        Attack("Tomoe-nage", 20, 50),
        Attack("Kesa-gatame Heal", 5, 20, special="heal")
    ], "Agarre y proyección"))

    pool.append(MartialArt("Aikido", [
        Attack("Ikkyo", 10, 20),
        Attack("Iriminage", 15, 30),
        Attack("Kokyu-ho Heal", 5, 20, special="heal")
    ], "Defensa y control"))

    pool.append(MartialArt("Capoeira", [
        Attack("Meia Lua", 10, 30),
        Attack("Armada", 15, 40),
        Attack("Ginga Extra", 10, 25, special="extra")
    ], "Movimiento y patadas"))

    pool.append(MartialArt("Krav Maga", [
        Attack("Hammerfist", 12, 32),
        Attack("Groin Kick", 20, 45),
        Attack("Counter Extra", 10, 25, special="extra")
    ], "Técnicas agresivas"))

    pool.append(MartialArt("Kickboxing", [
        Attack("Low Kick", 10, 25),
        Attack("High Kick", 20, 45),
        Attack("Combo Heal", 5, 20, special="heal")
    ], "Patadas y combos"))

    return pool
