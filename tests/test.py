"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - test
# ==========================================
#
#
# 
"""

import numpy as np
import pdf_maker as pm


file = pm.NewPDF(filepath="myPDF.pdf")

cv = pm.Canvas(width=17, height=12, unit="cm", show_frame=True, frame_line_width=1, clip_outside_plot_areas=False)

pt = cv.add_plot_area(name="Plot1", plot_area=(0.1, 0.1, 0.35, 0.35), plot_scale=(0, 200, 0, 200))
pt2 = cv.add_plot_area(name="Plot2", plot_area=(0.6, 0.1, 0.35, 0.35), plot_scale=(0, 200, 0, 200))
pt3 = cv.add_plot_area(name="Plot3", plot_area=(0.1, 0.6, 0.75, 0.35), plot_scale=(0, 200, 0, 200))

pt.text(name="TEXT01", x=50, y=50, text="hello", size=12, font="Arial", coordinate="scale")
pt2.text(name="TEXT02", x=40, y=70, text="hello", size=12, font="Arial", coordinate="scale")
pt3.text(name="TEXT03", x=40, y=70, text="hello", size=12, font="Arial", coordinate="scale")

for i in range(10):
    pt3.line(name=f"LINE_{i}", start=[0, i * 10], end=[300, i * 10 + 50], width=1, color="grey", line_style="solid")

xs = np.random.randint(low=0, high=200, size=10)
ys = np.random.randint(low=0, high=200, size=10)

for x, y in zip(xs, ys):
    pt.scatter(name=f"SCATTER_{x}_{y}", x=x, y=y, size=2, coordinate="scale", fill_color="red" if y <= 100 else "grey")

for x in range(0, 200, 50):
    pt.line(name=f"LINE_X_{x}", start=[x, 0], end=[x, 300], width=1, color="grey", line_style="dashed")
    pt2.line(name=f"LINE_X_{x}", start=[x, 0], end=[x, 300], width=1, color="grey", line_style="dashed")

for y in range(0, 200, 50):
    pt.line(name=f"LINE_Y_{y}", start=[0, y], end=[300, y], width=1, color="grey", line_style="dashdot")
    pt2.line(name=f"LINE_Y_{y}", start=[0, y], end=[300, y], width=1, color="grey", line_style="dashdot")

file.canvas(margin_left=1, margin_top=1, page=1, canvas=cv, unit="cm")

# save pdf
file.save()

print(file.content_str)

# import ararpy as ap
# # open ararpy files
# file_path = r'D:\PythonProjects\pdf-maker\venv\Lib\site-packages\ararpy\examples\22WHA0433.arr'
# sample = ap.from_arr(file_path=file_path)
