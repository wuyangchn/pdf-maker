"""
# ==========================================
# Copyright 2024 Yang 
# pdf-tool - test
# ==========================================
#
#
# 
"""


import pdf_tool as pt

file = pt.NewPDF(filepath="myPDF.pdf")

# write text to the given page

# draw lines to the given page
file.line(page=0, start=[100, 100], end=[300, 300], width=1, color="black")
file.line(page=0, start=[500, 100], end=[300, 300], width=5, color="red")

# draw a rectangle to the given page
file.rect(page=0, left_bottom=[100, 100], width=400, height=400, line_width=1, color="blue")

# draw scatters
for i in range(50):
    file.scatter(page=0, x=200 + i * 10, y=400 + i * 2, size=4)
    file.scatter(page=0, x=500 - i * 10, y=400 + i * 2, size=4, type="rectangle")

# save pdf
file.save()
