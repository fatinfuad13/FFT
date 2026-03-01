import tkinter as tk
import numpy as np
import math
from discrete_framework import DiscreteSignal, DFTAnalyzer,FastFourierTransform

class DoodlingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fourier Epicycles Doodler")
        
        # --- UI Layout ---
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()
        
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)
        
        # Buttons
        tk.Button(control_frame, text="Clear Canvas", command=self.clear).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Draw Epicycles", command=self.run_transform).pack(side=tk.LEFT, padx=5)
        
        # Toggle Switch (Radio Buttons)
        self.use_fft = tk.BooleanVar(value=False)
        tk.Label(control_frame, text=" |  Algorithm: ").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(control_frame, text="Naive DFT", variable=self.use_fft, value=False).pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="FFT", variable=self.use_fft, value=True).pack(side=tk.LEFT)

        # State Variables
        self.points = []
        self.drawing = False
        self.fourier_coeffs = None
        self.is_animating = False
        self.after_id = None

        # Bindings
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def start_draw(self, event):
        self.is_animating = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.canvas.delete("all")
        self.points = []
        self.drawing = True

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.points.append((x, y))
            r = 2
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black", outline="black")

    def end_draw(self, event):
        self.drawing = False

    def clear(self):
        self.canvas.delete("all")
        self.points = []
        self.is_animating = False
        if self.after_id:
            self.root.after_cancel(self.after_id)

    def draw_epicycle(self, x, y, radius):
        """
        Helper method for students to draw a circle (epicycle).
        x, y: Center coordinates
        radius: Radius of the circle
        """
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="blue", tags="epicycle")

    def run_transform(self):
        if not self.points: return
        
        # TODO: Implementation
        # 1. Convert (x,y) points to Complex Signal
        # 2. Select Algorithm 
        # 3. Compute Transform
        
        print("Number of points:", len(self.points))
        #print("Transform logic needed.")
        # self.animate_epicycles(mean_point)
        '''complex_points = np.array([complex(x,y) for x,y in self.points])
        signal = DiscreteSignal(complex_points)'''
        # Compute mean first
        x_points = [x for x,y in self.points]
        y_points = [y for x,y in self.points]

        mean_x = sum(x_points)/len(x_points)
        mean_y = sum(y_points)/len(y_points)

# Center drawing
        complex_points = np.array([
            complex(x - mean_x, y - mean_y)
            for x,y in self.points])

        signal = DiscreteSignal(complex_points)

        import time

        

        if self.use_fft.get():
            analyzer = FastFourierTransform()
            
            N = len(signal.data)
            lower = 1 << (N.bit_length() - 1)
            upper = 1 << N.bit_length()

            if N - lower < upper - N:
                next_pow2 = lower
            else:
                next_pow2 = upper

            signal = signal.interpolate(next_pow2)
        else:
            analyzer = DFTAnalyzer()
        
        start = time.time()
        spectrum = analyzer.compute_dft(signal)
        end = time.time()
        print(end-start)

        N = len(spectrum)

        #  Build frequency list with correct negative mapping
        self.fourier_coeffs = []

        for k in range(N):
            if k <= N // 2:
                freq = k
            else:
                freq = k - N

            amplitude = abs(spectrum[k]) / N
            phase = np.angle(spectrum[k])

            self.fourier_coeffs.append((freq, amplitude, phase))

        #  Sort by amplitude (largest circles first)
        self.fourier_coeffs.sort(key=lambda item: item[1], reverse=True)

        #  Compute drawing center
        '''x_points = [x for x,y in self.points]
        y_points = [y for x,y in self.points]

        mean_x = sum(x_points)/len(x_points)
        mean_y = sum(y_points)/len(y_points)'''

        self.num_frames = N
        self.animate_epicycles((mean_x,mean_y))

    def animate_epicycles(self, center_offset):
        self.is_animating = True
        self.time_step = 0
        # self.num_frames = ...
        
        self.center_offset = center_offset
        self.update_frame()

    def update_frame(self):
        if not self.is_animating:
                  return

        self.canvas.delete("epicycle")

        # TODO: Implementation
        # 1. Calculate the current time 't' based on self.time_step
        # 2. Reconstruct the signal value 'z' at time 't' 
        # 3. Draw the epicycles:
        # 4. Draw the tips

        t = self.time_step
        N = self.num_frames

        x,y = self.center_offset

        for (freq,radius,phase) in self.fourier_coeffs:
             prev_x, prev_y = x, y
             angle = 2 * np.pi * freq * t/N + phase

             x += radius * np.cos(angle)
             y += radius * np.sin(angle)

             self.draw_epicycle(prev_x, prev_y, radius)
             self.canvas.create_line(prev_x, prev_y, x, y, fill="red", tags="epicycle")

        r = 3
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="red", tags="epicycle")

        self.time_step = (self.time_step + 1)

        self.after_id = self.root.after(50, self.update_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = DoodlingApp(root)
    root.mainloop()