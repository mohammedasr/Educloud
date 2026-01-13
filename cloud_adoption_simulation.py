import random
import statistics
from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# ==========================
# ENUMS
# ==========================
class LocationType(Enum):
    URBAN = "urban"
    RURAL = "rural"


class Region(Enum):
    CENTRE = "Centre"
    LITTORAL = "Littoral"
    WEST = "West"
    NORTHWEST = "Northwest"
    SOUTHWEST = "Southwest"
    SOUTH = "South"
    EAST = "East"
    ADAMAWA = "Adamawa"
    NORTH = "North"
    FAR_NORTH = "Far North"


# ==========================
# DATA MODELS
# ==========================
@dataclass
class Infrastructure:
    internet_reliability: float = 0.0
    bandwidth_mbps: float = 0.0
    power_availability: float = 0.0
    device_per_student_ratio: float = 100.0

    def update(self, investment):
        self.internet_reliability = min(100, self.internet_reliability + random.uniform(3, 8) * investment)
        self.bandwidth_mbps = min(100, self.bandwidth_mbps + random.uniform(2, 6) * investment)
        self.power_availability = min(100, self.power_availability + random.uniform(2, 5) * investment)
        self.device_per_student_ratio = max(1, self.device_per_student_ratio - random.uniform(3, 7) * investment)


@dataclass
class TeacherCapability:
    digital_literacy: float = 20.0
    cloud_training: float = 0.0

    def update(self, intensity):
        self.digital_literacy = min(100, self.digital_literacy + random.uniform(5, 12) * intensity)
        self.cloud_training = min(100, self.cloud_training + random.uniform(8, 15) * intensity)


@dataclass
class School:
    location: LocationType
    infrastructure: Infrastructure = field(default_factory=Infrastructure)
    teacher: TeacherCapability = field(default_factory=TeacherCapability)
    adoption: float = 0.0

    def access(self):
        infra = (
            self.infrastructure.internet_reliability * 0.4 +
            min(self.infrastructure.bandwidth_mbps * 2, 100) * 0.3 +
            self.infrastructure.power_availability * 0.3
        ) / 100

        device = max(0, 1 - self.infrastructure.device_per_student_ratio / 100)
        teacher = (self.teacher.digital_literacy + self.teacher.cloud_training) / 200
        return min(100, (infra * 0.4 + device * 0.3 + teacher * 0.3) * 100)


# ==========================
# SIMULATION ENGINE
# ==========================
class SimulationEngine:
    def __init__(self, n=50):
        self.schools = []
        self.history = []
        self._create_schools(n)

    def _create_schools(self, n):
        for _ in range(n):
            loc = LocationType.URBAN if random.random() < 0.6 else LocationType.RURAL
            self.schools.append(School(loc))

    def simulate_year(self, investment):
        for s in self.schools:
            s.infrastructure.update(investment)
            s.teacher.update(investment)
            s.adoption = min(100, s.adoption + random.uniform(5, 12))

        urban = [s.access() for s in self.schools if s.location == LocationType.URBAN]
        rural = [s.access() for s in self.schools if s.location == LocationType.RURAL]

        metrics = {
            "access": statistics.mean(s.access() for s in self.schools),
            "adoption": statistics.mean(s.adoption for s in self.schools),
            "urban": statistics.mean(urban),
            "rural": statistics.mean(rural),
            "gap": statistics.mean(urban) - statistics.mean(rural)
        }
        self.history.append(metrics)
        return metrics


# ==========================
# GUI
# ==========================
class SimulationGUI:
    def __init__(self, root):
        self.root = root
        root.title("Cloud Adoption Simulation – Cameroon")
        root.geometry("1200x750")

        self._build_controls()
        self._build_output()
        self._build_charts()
        self._build_summary()

    # ---------- CONTROLS ----------
    def _build_controls(self):
        frame = ttk.LabelFrame(self.root, text="Simulation Controls")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Schools:").grid(row=0, column=0)
        self.school_var = tk.IntVar(value=50)
        ttk.Entry(frame, textvariable=self.school_var, width=8).grid(row=0, column=1)

        ttk.Label(frame, text="Scenario:").grid(row=0, column=2)
        self.scenario = tk.StringVar(value="Moderate")
        ttk.Combobox(
            frame,
            textvariable=self.scenario,
            values=["Low", "Moderate", "Aggressive", "Custom"],
            width=12,
            state="readonly"
        ).grid(row=0, column=3)

        self.run_btn = ttk.Button(frame, text="▶ Run", command=self.run)
        self.run_btn.grid(row=0, column=4, padx=10)

        ttk.Button(frame, text="💾 Export CSV", command=self.export).grid(row=0, column=5)

        self.progress = ttk.Progressbar(frame, length=300)
        self.progress.grid(row=1, column=0, columnspan=6, pady=5)

    # ---------- OUTPUT ----------
    def _build_output(self):
        frame = ttk.LabelFrame(self.root, text="Detailed Output")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.output = tk.Text(frame, font=("Consolas", 10))
        self.output.pack(fill="both", expand=True)

    # ---------- CHARTS ----------
    def _build_charts(self):
        frame = ttk.LabelFrame(self.root, text="Charts")
        frame.pack(fill="x", padx=10, pady=5)

        self.fig = Figure(figsize=(6, 3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- SUMMARY ----------
    def _build_summary(self):
        self.summary = ttk.Label(self.root, text="Run simulation to see summary.", font=("Segoe UI", 11, "bold"))
        self.summary.pack(pady=5)

    # ---------- RUN ----------
    def run(self):
        self.output.delete("1.0", tk.END)
        self.ax.clear()

        scenarios = {
            "Low": [0.5] * 5,
            "Moderate": [0.7, 0.9, 1.1, 1.3, 1.5],
            "Aggressive": [1.0, 1.3, 1.6, 1.8, 2.0],
        }

        schedule = scenarios.get(self.scenario.get(), [1.0] * 5)

        sim = SimulationEngine(self.school_var.get())
        access_vals = []
        adoption_vals = []

        for i, inv in enumerate(schedule, 1):
            self.progress["value"] = i * 20
            self.root.update_idletasks()

            m = sim.simulate_year(inv)
            access_vals.append(m["access"])
            adoption_vals.append(m["adoption"])

            self.output.insert(tk.END, f"YEAR {i}\n")
            self.output.insert(tk.END, f"  Access: {m['access']:.2f}%\n")
            self.output.insert(tk.END, f"  Adoption: {m['adoption']:.2f}%\n")
            self.output.insert(tk.END, f"  Urban–Rural Gap: {m['gap']:.2f}%\n\n")

        self.ax.plot(range(1, 6), access_vals, label="Student Access")
        self.ax.plot(range(1, 6), adoption_vals, label="Cloud Adoption")
        self.ax.legend()
        self.ax.set_title("5-Year Trends")
        self.canvas.draw()

        self.history = sim.history
        self.summary.config(
            text=f"Final Access: {access_vals[-1]:.2f}% | "
                 f"Final Adoption: {adoption_vals[-1]:.2f}%"
        )

    # ---------- EXPORT ----------
    def export(self):
        if not hasattr(self, "history"):
            messagebox.showwarning("No Data", "Run simulation first.")
            return

        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file:
            return

        with open(file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.history[0].keys())
            writer.writeheader()
            writer.writerows(self.history)

        messagebox.showinfo("Exported", "CSV exported successfully.")


# ==========================
# ENTRY POINT
# ==========================
if __name__ == "__main__":
    random.seed(42)
    root = tk.Tk()
    SimulationGUI(root)
    root.mainloop()
