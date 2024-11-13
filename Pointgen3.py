import tkinter as tk
from tkinter import filedialog


class PointExporterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Point Exporter")

        self.canvas_width = 1200
        self.canvas_height = 800
        self.grid_size_column = 60  # グリッドの列数
        self.grid_size_row = 40  # グリッドの行数

        self.canvas = tk.Canvas(
            master, width=self.canvas_width, height=self.canvas_height, bg="white"
        )
        self.canvas.pack()

        self.points = []
        self.selected_points = set()

        self.create_grid()

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.export_button = tk.Button(
            master, text="Export Selected Points", command=self.export_points
        )
        self.export_button.pack()

        self.selection_rect = None
        self.start_x = None
        self.start_y = None
        self.is_dragging = False

    def create_grid(self):
        x_step = self.canvas_width // (self.grid_size_column + 1)
        y_step = self.canvas_height // (self.grid_size_row + 1)

        for i in range(2, self.grid_size_column + 2):
            for j in range(2, self.grid_size_row + 2):
                x = i * x_step
                y = j * y_step
                point_id = self.canvas.create_oval(
                    x - 2, y - 2, x + 2, y + 2, fill="black", width=0
                )
                self.points.append((point_id, x, y))

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.is_dragging = False

        # 一点選択の処理
        clicked_point = self.find_clicked_point(self.start_x, self.start_y)
        if clicked_point:
            if not event.state & 0x4:  # Ctrlキーが押されていない場合
                self.clear_selection()
            self.toggle_point_selection(clicked_point)
        else:
            if not event.state & 0x4:
                self.clear_selection()  # クリアの処理

    def on_drag(self, event):
        if not self.is_dragging:
            self.is_dragging = True
            self.selection_rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, outline="blue"
            )

        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(
            self.selection_rect, self.start_x, self.start_y, cur_x, cur_y
        )

    def on_release(self, event):
        if self.is_dragging:
            end_x = self.canvas.canvasx(event.x)
            end_y = self.canvas.canvasy(event.y)
            self.canvas.delete(self.selection_rect)
            self.selection_rect = None

            x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
            x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)

            if not event.state & 0x4:  # Ctrlキーが押されていない場合
                self.clear_selection()

            for point_id, x, y in self.points:
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.selected_points.add(point_id)
                    self.canvas.itemconfig(point_id, fill="red")

        self.is_dragging = False

    def find_clicked_point(self, x, y):
        for point_id, px, py in self.points:
            if abs(x - px) < 5 and abs(y - py) < 5:
                return point_id
        return None

    def toggle_point_selection(self, point_id):
        if point_id in self.selected_points:
            self.selected_points.remove(point_id)
            self.canvas.itemconfig(point_id, fill="black")
        else:
            self.selected_points.add(point_id)
            self.canvas.itemconfig(point_id, fill="red")

    def clear_selection(self):
        for point_id in self.selected_points:
            self.canvas.itemconfig(point_id, fill="black")
        self.selected_points.clear()

    def export_points(self):
        if not self.selected_points:
            print("No points selected")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".prof")
        if not filename:
            return

        with open(filename, "w") as f:
            for point_id, x, y in self.points:
                if point_id in self.selected_points:
                    f.write(f"{x}  {y}  0\n")

        print(f"Exported {len(self.selected_points)} points to {filename}")


root = tk.Tk()
app = PointExporterApp(root)
root.mainloop()
