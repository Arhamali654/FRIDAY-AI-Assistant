import customtkinter as ctk
import threading
import datetime
import time
import math
import random
import sys
sys.path.insert(0, "F:\\JARVIS")
from config import JARVIS_NAME

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FridayDashboard:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(f"{JARVIS_NAME} — AI Assistant")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        self.root.configure(fg_color="#020408")

        self.is_listening   = False
        self.is_speaking    = False
        self.always_listen  = True
        self.angle          = 0
        self.pulse          = 0
        self.particles      = []

        self._init_particles()
        self._build_ui()
        self._start_clock()
        self._start_animations()
        self.root.after(1500, self._welcome)
        self.root.after(3000, self._start_always_listen)

    def _init_particles(self):
        for _ in range(40):
            self.particles.append({
                "x":  random.uniform(0, 340),
                "y":  random.uniform(0, 400),
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-0.3, 0.3),
                "size": random.uniform(1, 3),
                "alpha": random.uniform(0.2, 0.8)
            })

    def _welcome(self):
        def _say():
            from modules.voice import speak
            from modules.memory import save_conversation
            msg = "Welcome Boss. FRIDAY online and fully operational. How can I assist you today?"
            self.add_message(JARVIS_NAME, msg)
            self.is_speaking = True
            speak(msg)
            self.is_speaking = False
        threading.Thread(target=_say, daemon=True).start()

    def _start_always_listen(self):
        if self.always_listen:
            threading.Thread(target=self._always_listen_loop, daemon=True).start()

    def _always_listen_loop(self):
        from modules.voice import listen
        while self.always_listen:
            if not self.is_speaking and not self.is_listening:
                self.is_listening = True
                self.set_status("Listening...", "#00ff66")
                try:
                    command = listen(timeout=6, phrase_limit=15)
                    if command and command.strip():
                        self.is_listening = False
                        self.add_message("YOU", command)
                        self._run_command(command)
                    else:
                        self.is_listening = False
                        self.set_status("Ready.", "#0a2233")
                except Exception as e:
                    self.is_listening = False
                    self.set_status("Ready.", "#0a2233")
            time.sleep(0.3)

    def _build_ui(self):
        top_bar = ctk.CTkFrame(self.root, fg_color="#020810", height=56, corner_radius=0)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        ctk.CTkLabel(
            top_bar, text=f"◈  {JARVIS_NAME}",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#00d4ff"
        ).pack(side="left", padx=24, pady=10)

        ctk.CTkLabel(
            top_bar, text="STARK INDUSTRIES  //  PERSONAL AI",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#1a3344"
        ).pack(side="left")

        self.clock_label = ctk.CTkLabel(
            top_bar, text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#1a4455"
        )
        self.clock_label.pack(side="right", padx=20)

        self.status_dot = ctk.CTkLabel(
            top_bar, text="◉  ONLINE",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#00ff88"
        )
        self.status_dot.pack(side="right", padx=16)

        main = ctk.CTkFrame(self.root, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=14, pady=10)

        left = ctk.CTkFrame(main, fg_color="#020810", corner_radius=14, width=340)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        ctk.CTkLabel(
            left, text="CORE",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#0a2233"
        ).pack(anchor="w", padx=16, pady=(14, 0))

        self.canvas = ctk.CTkCanvas(
            left, width=310, height=310,
            bg="#020810", highlightthickness=0
        )
        self.canvas.pack(padx=14, pady=10)

        self.state_label = ctk.CTkLabel(
            left, text="STANDBY",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#1a4455"
        )
        self.state_label.pack(pady=(0, 4))

        self.listen_toggle = ctk.CTkSwitch(
            left,
            text="Always listening",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#336677",
            command=self._toggle_listen,
            onvalue=True, offvalue=False
        )
        self.listen_toggle.select()
        self.listen_toggle.pack(pady=(0, 6))

        ctk.CTkLabel(
            left, text="QUICK ACCESS",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#0a2233"
        ).pack(anchor="w", padx=16, pady=(8, 4))

        quick = [
            ("📊 System stats",  "system stats"),
            ("🌤 Weather",        "what's the weather"),
            ("📰 Latest news",    "latest news"),
            ("📷 Screenshot",     "take a screenshot"),
            ("🎵 Play music",     "play music"),
            ("⏸ Pause music",    "pause music"),
            ("🌐 Open Chrome",    "open chrome"),
            ("🗒 Open Notepad",   "open notepad"),
        ]
        for label, cmd in quick:
            ctk.CTkButton(
                left, text=label, height=32,
                fg_color="#020c14", hover_color="#041828",
                text_color="#336677",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                corner_radius=6, anchor="w",
                command=lambda c=cmd: self._run_command(c)
            ).pack(fill="x", padx=14, pady=2)

        ctk.CTkButton(
            left, text="🗑  Clear chat", height=30,
            fg_color="#1a0505", hover_color="#2a0808",
            text_color="#663333",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            corner_radius=6, command=self._clear_chat
        ).pack(fill="x", padx=14, pady=(10, 14))

        right = ctk.CTkFrame(main, fg_color="#020810", corner_radius=14)
        right.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            right, text="CONVERSATION LOG",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#0a2233"
        ).pack(anchor="w", padx=16, pady=(14, 4))

        self.chat_box = ctk.CTkTextbox(
            right,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="#010509", text_color="#88aacc",
            border_color="#061020", border_width=1,
            corner_radius=10, wrap="word", state="disabled"
        )
        self.chat_box.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        inp = ctk.CTkFrame(right, fg_color="transparent")
        inp.pack(fill="x", padx=12, pady=(0, 14))

        self.input_box = ctk.CTkEntry(
            inp,
            placeholder_text="Or type a command here...",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="#010509", border_color="#061020",
            text_color="#88aacc", height=42, corner_radius=10
        )
        self.input_box.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.input_box.bind("<Return>", lambda e: self._on_send())

        ctk.CTkButton(
            inp, text="SEND", width=80, height=42,
            fg_color="#001a2e", hover_color="#002a44",
            text_color="#00d4ff",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=10, border_width=1, border_color="#003355",
            command=self._on_send
        ).pack(side="left")

        bot = ctk.CTkFrame(self.root, fg_color="#020810", height=30, corner_radius=0)
        bot.pack(fill="x", side="bottom")
        bot.pack_propagate(False)

        self.bottom_status = ctk.CTkLabel(
            bot, text=f"  {JARVIS_NAME} ready.",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#0a2233"
        )
        self.bottom_status.pack(side="left", padx=10)

        ctk.CTkLabel(
            bot, text="SYSTEM NOMINAL  //  ALL MODULES ACTIVE  ",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color="#0a2233"
        ).pack(side="right")

    def _toggle_listen(self):
        self.always_listen = self.listen_toggle.get()
        if self.always_listen:
            self._start_always_listen()

    def _start_clock(self):
        def _tick():
            while True:
                now = datetime.datetime.now().strftime("%A %d %B %Y   %H:%M:%S")
                self.clock_label.configure(text=now)
                time.sleep(1)
        threading.Thread(target=_tick, daemon=True).start()

    def _start_animations(self):
        self._animate()

    def _animate(self):
        self.angle = (self.angle + 1.2) % 360
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)
        cx, cy, r  = 155, 155, 100
        self.canvas.delete("all")

        for p in self.particles:
            p["x"] += p["vx"]; p["y"] += p["vy"]
            if p["x"] < 0 or p["x"] > 310: p["vx"] *= -1
            if p["y"] < 0 or p["y"] > 310: p["vy"] *= -1
            alpha = int(p["alpha"] * 255)
            color = f"#{0:02x}{int(alpha*0.4):02x}{int(alpha*0.7):02x}"
            self.canvas.create_oval(
                p["x"]-p["size"], p["y"]-p["size"],
                p["x"]+p["size"], p["y"]+p["size"],
                fill=color, outline=""
            )

        pulse_r = math.sin(self.pulse) * 8

        for radius, color, width in [
            (r+40+pulse_r, "#001a2e", 1),
            (r+28,         "#002233", 1),
            (r+14,         "#003344", 1),
        ]:
            self.canvas.create_oval(
                cx-radius, cy-radius, cx+radius, cy+radius,
                outline=color, width=width
            )

        if self.is_listening:
            arc_color = "#00ff66"
            arc_speed = self.angle * 3
        elif self.is_speaking:
            arc_color = "#ffaa00"
            arc_speed = self.angle * 2
        else:
            arc_color = "#00d4ff"
            arc_speed = self.angle

        self.canvas.create_arc(
            cx-r-14, cy-r-14, cx+r+14, cy+r+14,
            start=arc_speed, extent=240,
            outline=arc_color, width=2, style="arc"
        )
        self.canvas.create_arc(
            cx-r-14, cy-r-14, cx+r+14, cy+r+14,
            start=arc_speed+240, extent=60,
            outline="#001a2e", width=2, style="arc"
        )
        self.canvas.create_arc(
            cx-r-8, cy-r-8, cx+r+8, cy+r+8,
            start=-arc_speed, extent=180,
            outline="#001a33", width=1, style="arc"
        )

        glow_r = r + pulse_r * 0.5
        for g_r, opacity in [(glow_r, 0.08), (glow_r*0.7, 0.15), (glow_r*0.4, 0.3)]:
            intensity = int(opacity * 255)
            color = f"#{0:02x}{intensity:02x}{min(255,intensity*2):02x}"
            self.canvas.create_oval(
                cx-g_r, cy-g_r, cx+g_r, cy+g_r,
                fill=color, outline=""
            )

        self.canvas.create_oval(
            cx-r+2, cy-r+2, cx+r-2, cy+r-2,
            outline=arc_color, width=2
        )

        hex_r  = 38
        points = []
        for i in range(6):
            a = math.radians(60*i + self.angle*0.3)
            points.extend([cx + hex_r*math.cos(a), cy + hex_r*math.sin(a)])
        self.canvas.create_polygon(points, outline="#004466", fill="", width=1)

        dot_r = 14 + math.sin(self.pulse*2) * 2
        self.canvas.create_oval(
            cx-dot_r, cy-dot_r, cx+dot_r, cy+dot_r,
            fill="#001a2e", outline=arc_color, width=2
        )
        self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill=arc_color, outline="")

        for i in range(24):
            a  = math.radians(i * 15 + self.angle * 0.2)
            r1 = r + 18
            r2 = r + 22 if i % 6 == 0 else r + 20
            self.canvas.create_line(
                cx+r1*math.cos(a), cy+r1*math.sin(a),
                cx+r2*math.cos(a), cy+r2*math.sin(a),
                fill="#002233", width=1
            )

        self.root.after(33, self._animate)

    def add_message(self, sender: str, message: str):
        self.chat_box.configure(state="normal")
        now = datetime.datetime.now().strftime("%H:%M:%S")
        if sender == "YOU":
            self.chat_box.insert("end", f"\n  [{now}]  YOU\n")
            self.chat_box.insert("end", f"  {message}\n")
        else:
            self.chat_box.insert("end", f"\n  [{now}]  {JARVIS_NAME}\n")
            self.chat_box.insert("end", f"  {message}\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def set_status(self, text: str, color: str = "#0a2233"):
        self.bottom_status.configure(text=f"  {text}", text_color=color)
        self.state_label.configure(text=text.upper(), text_color=color)

    def _run_command(self, command: str):
        self.set_status("Processing...", "#00d4ff")
        self.is_speaking = True
        def _process():
            try:
                from main import route_command
                from modules.memory import save_conversation
                from modules.voice import speak
                response = route_command(command)
                self.add_message(JARVIS_NAME, response)
                self.set_status("Speaking...", "#ffaa00")
                speak(response)
                self.is_speaking = False
                self.set_status("Listening...", "#00ff66")
                save_conversation(command, response)
            except Exception as e:
                self.add_message(JARVIS_NAME, f"Error: {e}")
                self.set_status("Error.", "#ff4444")
                self.is_speaking = False
        threading.Thread(target=_process, daemon=True).start()

    def _on_send(self):
        command = self.input_box.get().strip()
        if command:
            self.input_box.delete(0, "end")
            self.add_message("YOU", command)
            self._run_command(command)

    def _clear_chat(self):
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")
        self.chat_box.configure(state="disabled")

    def run(self):
        self.root.mainloop()


def launch_dashboard():
    app = FridayDashboard()
    app.run()


if __name__ == "__main__":
    launch_dashboard()
