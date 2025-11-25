# gui_animated.py
import tkinter as tk
from tkinter import ttk, messagebox
import random
from models import Player, create_arts_pool, MartialArt

ANIM_STEP = 8      # pixels per frame for attack move
ANIM_DELAY = 20    # ms between frames
DAMAGE_POP_LIFETIME = 800  # ms the floating damage text stays

class AnimatedGUI:
    def __init__(self, root):
        self.root = root
        root.title("Caso 3 - Strategy (Animado)")

        # modelo
        self.pool = create_arts_pool()
        self.p1 = Player("Jugador 1")
        self.p2 = Player("Jugador 2")
        self.p1.assign_random_arts(self.pool)
        self.p2.assign_random_arts(self.pool)

        # estado
        self.current_turn = 1  # 1 o 2
        self.is_animating = False

        # canvas (escena)
        self.canvas = tk.Canvas(root, width=900, height=300, bg="#1e1e2e")
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=8)

        # dibujar personajes (rectángulos simples como sprites placeholder)
        self.p1_sprite = self.canvas.create_rectangle(80, 120, 180, 220, fill="#4CAF50", outline="white", width=2)
        self.p2_sprite = self.canvas.create_rectangle(720, 120, 820, 220, fill="#F44336", outline="white", width=2)

        # nombres
        self.canvas.create_text(130, 100, text=self.p1.name, fill="white", font=("Arial", 10, "bold"))
        self.canvas.create_text(770, 100, text=self.p2.name, fill="white", font=("Arial", 10, "bold"))

        # health bars background
        self.p1_hp_bg = self.canvas.create_rectangle(40, 230, 220, 250, fill="#333", outline="")
        self.p2_hp_bg = self.canvas.create_rectangle(680, 230, 860, 250, fill="#333", outline="")

        # health bars foreground (variable width)
        self.p1_hp_fg = self.canvas.create_rectangle(40, 230, 220, 250, fill="#76FF03", outline="")
        self.p2_hp_fg = self.canvas.create_rectangle(680, 230, 860, 250, fill="#FF5252", outline="")

        # panel lateral (controles)
        control = ttk.Frame(root, padding=8)
        control.grid(row=1, column=0, sticky="n")

        # P1 controls
        ttk.Label(control, text=self.p1.name, font=("Arial", 10, "bold")).grid(row=0, column=0)
        self.p1_choice = tk.StringVar()
        self.p1_map = {a.name: a for a in self.p1.arts}
        self.p1_combo = ttk.Combobox(control, textvariable=self.p1_choice, values=list(self.p1_map.keys()), state="readonly", width=25)
        self.p1_combo.current(0)
        self.p1_combo.grid(row=1, column=0, pady=2)
        self.p1_combo.bind("<<ComboboxSelected>>", lambda e: self.show_p1_attacks())

        ttk.Label(control, text="Golpes:").grid(row=2, column=0)
        self.p1_attacks = tk.Text(control, width=30, height=6)
        self.p1_attacks.grid(row=3, column=0)
        ttk.Button(control, text="Atacar (Jugador 1)", command=lambda: self.request_attack(1)).grid(row=4, column=0, pady=4)
        ttk.Button(control, text="Reasignar (Jugador 1)", command=lambda: self.reassign(self.p1, player_id=1)).grid(row=5, column=0, pady=2)

        # center controls
        center = ttk.Frame(root, padding=8)
        center.grid(row=1, column=1, sticky="n")
        self.turn_label = tk.StringVar(value="Turno: Jugador 1")
        ttk.Label(center, textvariable=self.turn_label, font=("Arial", 12, "bold")).grid(row=0, column=0, pady=6)
        ttk.Button(center, text="Turno Auto (Ataca y pasa turno)", command=self.auto_turn).grid(row=1, column=0, pady=4)
        ttk.Button(center, text="Guardar bitácora", command=self.save_log).grid(row=2, column=0, pady=2)

        # P2 controls
        right = ttk.Frame(root, padding=8)
        right.grid(row=1, column=2, sticky="n")
        ttk.Label(right, text=self.p2.name, font=("Arial", 10, "bold")).grid(row=0, column=0)
        self.p2_choice = tk.StringVar()
        self.p2_map = {a.name: a for a in self.p2.arts}
        self.p2_combo = ttk.Combobox(right, textvariable=self.p2_choice, values=list(self.p2_map.keys()), state="readonly", width=25)
        self.p2_combo.current(0)
        self.p2_combo.grid(row=1, column=0, pady=2)
        self.p2_combo.bind("<<ComboboxSelected>>", lambda e: self.show_p2_attacks())

        ttk.Label(right, text="Golpes:").grid(row=2, column=0)
        self.p2_attacks = tk.Text(right, width=30, height=6)
        self.p2_attacks.grid(row=3, column=0)
        ttk.Button(right, text="Atacar (Jugador 2)", command=lambda: self.request_attack(2)).grid(row=4, column=0, pady=4)
        ttk.Button(right, text="Reasignar (Jugador 2)", command=lambda: self.reassign(self.p2, player_id=2)).grid(row=5, column=0, pady=2)

        # bitácora (abajo)
        self.log_text = tk.Text(root, width=120, height=8)
        self.log_text.grid(row=2, column=0, columnspan=3, padx=10, pady=6)
        self._log("Juego animado iniciado. Selecciona técnica y ataca.")

        # inicializar vistas
        self.show_p1_attacks()
        self.show_p2_attacks()
        self.update_health_bars()

    # ------------ helpers: show attacks ----------------
    def show_p1_attacks(self):
        name = self.p1_choice.get()
        art = self.p1_map.get(name)
        self.p1_attacks.delete("1.0", tk.END)
        if art:
            for a in art.attacks:
                special = f" [{a.special}]" if a.special else ""
                self.p1_attacks.insert(tk.END, f"{a.name}: {a.min_power}-{a.max_power}{special}\n")

    def show_p2_attacks(self):
        name = self.p2_choice.get()
        art = self.p2_map.get(name)
        self.p2_attacks.delete("1.0", tk.END)
        if art:
            for a in art.attacks:
                special = f" [{a.special}]" if a.special else ""
                self.p2_attacks.insert(tk.END, f"{a.name}: {a.min_power}-{a.max_power}{special}\n")

    # ------------ reassign ---------------
    def reassign(self, player: Player, player_id: int = 1):
        player.assign_random_arts(self.pool)
        if player_id == 1:
            self.p1_map = {a.name: a for a in player.arts}
            self.p1_combo['values'] = list(self.p1_map.keys())
            self.p1_combo.current(0)
            self.show_p1_attacks()
            self._log(f"{player.name} reasignó artes: {', '.join(a.name for a in player.arts)}")
        else:
            self.p2_map = {a.name: a for a in player.arts}
            self.p2_combo['values'] = list(self.p2_map.keys())
            self.p2_combo.current(0)
            self.show_p2_attacks()
            self._log(f"{player.name} reasignó artes: {', '.join(a.name for a in player.arts)}")
        self.update_health_bars()

    # ------------ request attack (validación de turno) -------------
    def request_attack(self, player_id: int):
        if self.is_animating:
            return  # evitar colisiones de animación

        if player_id != self.current_turn:
            messagebox.showwarning("Turno equivocado", "No es tu turno.")
            return

        # obtener attacker y defender y arte seleccionada
        if player_id == 1:
            attacker = self.p1
            defender = self.p2
            art_name = self.p1_choice.get()
            art = self.p1_map.get(art_name)
            attacker_sprite = self.p1_sprite
            defender_sprite = self.p2_sprite
        else:
            attacker = self.p2
            defender = self.p1
            art_name = self.p2_choice.get()
            art = self.p2_map.get(art_name)
            attacker_sprite = self.p2_sprite
            defender_sprite = self.p1_sprite

        if art is None:
            messagebox.showerror("Error", "Selecciona una técnica válida.")
            return

        hits = random.randint(3,6)
        # lanzar animación -> cuando termine la animación se aplica el daño real y se actualiza UI
        self.animate_attack(attacker, defender, art, hits, attacker_sprite, defender_sprite)

    # ------------ animate attack sequence -------------
    def animate_attack(self, attacker, defender, art: MartialArt, hits: int, atk_sprite, def_sprite):
        self.is_animating = True
        # posicion actual de sprites
        atk_coords = self.canvas.coords(atk_sprite)
        def_coords = self.canvas.coords(def_sprite)

        # calcular dirección: si atk a la izquierda, se mueve a la derecha; si a la derecha, mueve a la izquierda
        atk_center_x = (atk_coords[0] + atk_coords[2]) / 2
        def_center_x = (def_coords[0] + def_coords[2]) / 2
        direction = 1 if def_center_x > atk_center_x else -1

        target_x = def_center_x - direction * 140  # posición frontal (justo antes del rival)
        # animar avance
        def advance():
            nonlocal atk_coords
            if direction == 1:
                if self.canvas.coords(atk_sprite)[2] < target_x:
                    self.canvas.move(atk_sprite, ANIM_STEP, 0)
                    self.root.after(ANIM_DELAY, advance)
                else:
                    self.show_hit_effects(attacker, defender, art, hits, atk_sprite, def_sprite)
            else:
                if self.canvas.coords(atk_sprite)[0] > target_x:
                    self.canvas.move(atk_sprite, -ANIM_STEP, 0)
                    self.root.after(ANIM_DELAY, advance)
                else:
                    self.show_hit_effects(attacker, defender, art, hits, atk_sprite, def_sprite)

        advance()

    # ------------ show hit effects (floating damage) then retreat -----------
    def show_hit_effects(self, attacker, defender, art: MartialArt, hits: int, atk_sprite, def_sprite):
        # Mostrar texto de la técnica
        self._log(f"{attacker.name} usa '{art.name}' ({hits} golpes)")

        # Para cada golpe, mostrar numero flotante rápido (visual) y aplicar lógica con pequeña separación
        idx = 0
        def do_one_hit():
            nonlocal idx
            if idx >= hits:
                # terminado: retroceder y terminar animación
                self.root.after(200, lambda: self.retreat(attacker, defender, atk_sprite, def_sprite))
                return

            # elegir ataque visual (no aplica valores aun) para mostrar
            attack = random.choice(art.attacks)
            # posición del defensor para mostrar número
            def_coords = self.canvas.coords(def_sprite)
            x = (def_coords[0] + def_coords[2]) / 2
            y = def_coords[1] - 10 - idx*6
            dmg_text = self.canvas.create_text(x, y, text=f"-{random.randint(attack.min_power, attack.max_power)}", fill="yellow", font=("Arial", 12, "bold"))
            # animación de desaparición
            self.root.after(DAMAGE_POP_LIFETIME, lambda: self.canvas.delete(dmg_text))

            # también pulso el borde del sprite (flash)
            orig_outline = self.canvas.itemcget(def_sprite, "outline")
            self.canvas.itemconfig(def_sprite, outline="white")
            self.root.after(120, lambda: self.canvas.itemconfig(def_sprite, outline=orig_outline))

            idx += 1
            # next hit visual
            self.root.after(180, do_one_hit)

        do_one_hit()

        # Aplicar la lógica real de los hits (usando perform_hits) después de mostrar los efectos visuales (pequeño delay)
        self.root.after( (hits * 180) + 220, lambda: self.apply_hits_and_update(attacker, defender, art, hits))

    # ------------ apply hits logic, update bars ----------
    def apply_hits_and_update(self, attacker, defender, art: MartialArt, hits: int):
        # aplicar lógica real (actualiza vida y bitácora)
        art.perform_hits(attacker, defender, hits, self._log)
        # actualizar barras de vida con animación suave
        self.update_health_bars(animated=True)
        # marcar animación completada (retreat se encarga de permitir nuevas acciones)
        # retreat se encarga del cambio de turno

    # ------------ retreat (regresar atacante a su posición) -----------
    def retreat(self, attacker, defender, atk_sprite, def_sprite):
        # mover el atacante de regreso a su inicio
        # determinar original target: left or right area
        if attacker is self.p1:
            target_x = 80
        else:
            target_x = 720

        def move_back():
            x1, y1, x2, y2 = self.canvas.coords(atk_sprite)
            current_center = (x1 + x2) / 2
            # mover hacia target center
            if current_center < target_x + 50:
                self.canvas.move(atk_sprite, ANIM_STEP, 0)
                self.root.after(ANIM_DELAY, move_back)
            elif current_center > target_x + 50:
                self.canvas.move(atk_sprite, -ANIM_STEP, 0)
                self.root.after(ANIM_DELAY, move_back)
            else:
                # finalizado: liberar animación y cambiar turno
                self.is_animating = False
                self.current_turn = 2 if self.current_turn == 1 else 1
                self.update_turn_label()
        move_back()

    # ------------ update health bars (animated) -------------
    def update_health_bars(self, animated: bool = False):
        # compute widths (max width 180)
        max_w = 180
        def set_bar(fg_item, life):
            target_w = 40 + (life / 200) * max_w  # 40..220 area
            x1, y1, x2, y2 = self.canvas.coords(fg_item)
            if animated:
                # animate width change
                def step():
                    nonlocal x2
                    x1, y1, x2_curr, y2 = self.canvas.coords(fg_item)
                    curr_w = x2_curr
                    # compute current width center x2 - approach target
                    if abs(x2_curr - target_w) > 2:
                        new_x2 = x2_curr + (target_w - x2_curr) * 0.25
                        # clamp
                        if new_x2 < 40: new_x2 = 40
                        if new_x2 > 220: new_x2 = 220
                        self.canvas.coords(fg_item, 40, 230, new_x2, 250)
                        self.root.after(40, step)
                step()
            else:
                self.canvas.coords(fg_item, 40, 230, target_w, 250)

        set_bar(self.p1_hp_fg, self.p1.life)
        # p2 bar uses different coordinates (680..860)
        def set_bar_p2(fg_item, life):
            target_w = 860 - ( (200 - life) / 200 * 180 )  # map to 680..860 (we'll set right edge)
            # But easier: compute left = 680, right = 680 + (life/200)*180
            right = 680 + (life / 200) * 180
            if animated:
                def step2():
                    x1, y1, x2_curr, y2 = self.canvas.coords(fg_item)
                    if abs(x2_curr - right) > 2:
                        new_x2 = x2_curr + (right - x2_curr) * 0.25
                        if new_x2 < 680: new_x2 = 680
                        if new_x2 > 860: new_x2 = 860
                        self.canvas.coords(fg_item, 680, 230, new_x2, 250)
                        self.root.after(40, step2)
                step2()
            else:
                self.canvas.coords(fg_item, 680, 230, right, 250)

        set_bar(self.p1_hp_fg, self.p1.life)
        set_bar_p2(self.p2_hp_fg, self.p2.life)
        # update labels too
        self.turn_label.set(f"Turno: Jugador {self.current_turn} | Vida P1: {self.p1.life}  P2: {self.p2.life}")

    # ------------ apply hits and then probably end  ----------
    def apply_hits_and_update(self, attacker, defender, art, hits):
        art.perform_hits(attacker, defender, hits, self._log)
        self.update_health_bars(animated=True)
        # check end of game
        if not defender.is_alive():
            self._log(f"--- {attacker.name} GANÓ! {defender.name} quedó en 0 vida ---")
            messagebox.showinfo("Fin del juego", f"{attacker.name} ganó. Reinicie la app.")
            self.is_animating = False
            # disable controls by setting turn to 0
            self.current_turn = 0
            self.update_health_bars()
            return
        # else: allow retreat to switch turn (retreat will flip turn)

    def update_turn_label(self):
        self.turn_label.set(f"Turno: Jugador {self.current_turn} | Vida P1: {self.p1.life}  P2: {self.p2.life}")

    # auto turn (current performs one attack)
    def auto_turn(self):
        if self.current_turn == 0 or self.is_animating:
            return
        self.request_attack(self.current_turn)

    def _log(self, text: str):
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def save_log(self):
        with open("bitacora_caso3_animada.txt", "a", encoding="utf-8") as f:
            f.write(self.log_text.get("1.0", tk.END))
        messagebox.showinfo("Guardado", "Bitácora guardada en bitacora_caso3_animada.txt")
