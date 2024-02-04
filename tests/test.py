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

cv = pm.Canvas(width=250, height=200, scale=(0, 100, 0, 200), show_frame=True)

cv.text(name="TEXT01", x=50, y=50, text="hello", size=12, font="arial", coordinate="scale")

xs = np.random.randint(low=5, high=85, size=100)
ys = np.random.randint(low=5, high=200, size=100)
for x, y in zip(xs, ys):
    cv.scatter(name=f"SCATTER_{x}_{y}", x=x, y=y, size=2, coordinate="scale", fill_color="red" if y <= 100 else "grey")


for x in range(0, 100):
    cv.line(name=f"LINE_X_{x}", start=[x, 0], end=[x, 200], width=0.5, color="grey")

for y in range(0, 200):
    cv.line(name=f"LINE_Y_{y}", start=[0, y], end=[100, y], width=0.5, color="grey")

file.canvas(margin_left=150, margin_top=100, page=1, canvas=cv)

# save pdf
file.save()



