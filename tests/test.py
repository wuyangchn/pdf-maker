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
import ararpy as ap


file = pm.NewPDF(filepath="myPDF.pdf")

cv = pm.Canvas(width=15, height=12, unit="cm", show_frame=True, frame_line_width=1,
               plot_area=(0.2, 0.2, 0.7, 0.7), plot_scale=(0, 200, 0, 200))

pt = cv.plot_area()

pt.text(name="TEXT01", x=50, y=50, text="hello", size=12, font="helvetica", coordinate="scale")

xs = np.random.randint(low=0, high=200, size=100)
ys = np.random.randint(low=0, high=200, size=100)

for x, y in zip(xs, ys):
    pt.scatter(name=f"SCATTER_{x}_{y}", x=x, y=y, size=2, coordinate="scale", fill_color="red" if y <= 100 else "grey")

for x in range(0, 200, 50):
    pt.line(name=f"LINE_X_{x}", start=[x, 0], end=[x, 300], width=1, color="grey", line_style="dashed")

for y in range(0, 200, 50):
    pt.line(name=f"LINE_Y_{y}", start=[0, y], end=[300, y], width=1, color="grey", line_style="dashdot")

file.canvas(margin_left=1, margin_top=1, page=1, canvas=cv, unit="cm")

# save pdf
file.save()

print(file.content_str)

# print(file.get_obj(type="FontDescriptor")[0].data())

# open ararpy files
file_path = r'D:\PythonProjects\pdf-maker\venv\Lib\site-packages\ararpy\examples\22WHA0433.arr'
sample = ap.from_arr(file_path=file_path)
