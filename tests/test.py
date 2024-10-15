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


def test_create_a_pdf():

    file = pm.NewPDF(filepath="myPDF_for_cdr_test_2.pdf")
    # as default, an empty pdf will have one page
    file.line(page=1, start=(10, 800), end=(10, 10), width=0.1)
    color = '#cd0000'
    file.line(page=1, start=(10, 700), end=(20, 690), width=1, line_caps="square", color=color)
    file.line(page=1, start=(10, 700), end=(20, 710), width=1, line_caps="square", color=color)
    color = '#49ae1d'
    file.line(page=1, start=(10, 600), end=(0, 610), width=1, line_caps="square", color=color)
    file.line(page=1, start=(10, 600), end=(0, 590), width=1, line_caps="square", color=color)

    file.add_page()
    # create a canvas
    color = '#ff5e14'
    cv = pm.Canvas(width=17, height=12, unit="cm", show_frame=True, frame_line_width=1, color=color,
                   clip_outside_plot_areas=False)

    # add plot areas to the canvas and define coordinate scale,
    # the position and widths and heights of the plot area are defined relative to the canvas
    # plot_area = (margin_to_left, margin_to_bottom, width, height), plot_scale = (xMin, xMax, yMix, yMax)
    color = '#549aab'
    pt = cv.add_plot_area(name="Plot1", plot_area=[0.1, 0.1, 0.35, 0.35], plot_scale=[0, 200, 0, 200], color=color,
                          show_frame=True)
    # pt2 = cv.add_plot_area(name="Plot2", plot_area=(0.6, 0.1, 0.35, 0.35), plot_scale=(0, 200, 0, 200), show_frame=True)
    # pt3 = cv.add_plot_area(name="Plot3", plot_area=(0.12, 0.6, 0.75, 0.35), plot_scale=(0, 200, 0, 200), show_frame=True)
    #
    # pt.line(start=(-10, 50), end=(-10, 100), width=1, coordinate="scale")
    # pt.line(start=(50, 210), end=(70, 210), width=1, coordinate="scale")
    l = pt.line(start=(50, 50), end=(600, 400), width=1, coordinate="scale", clip=True, x_clip=False, y_clip=True)
    l = pt.line(start=(50, 50), end=(600, 400), color='red', width=1, coordinate="scale", clip=True, x_clip=True, y_clip=False)
    l = pt.line(start=(50, 50), end=(400, 600), width=1, coordinate="scale", clip=True, x_clip=True, y_clip=False)
    l = pt.line(start=(50, 50), end=(400, 600), color='red', width=1, coordinate="scale", clip=True, x_clip=False, y_clip=True)

    l = pt.line(start=(150, 50), end=(600, 50), width=1, coordinate="scale", clip=True, x_clip=False, y_clip=True)
    l = pt.line(start=(150, 50), end=(600, 50), color='red', width=1, coordinate="scale", clip=True, y_clip=False)

    l = pt.line(start=(150, 100), end=(150, 400), width=1, coordinate="scale", clip=True, x_clip=True, y_clip=False)
    l = pt.line(start=(150, 100), end=(150, 400), color='red', width=1, coordinate="scale", clip=True)
    l = pt.line(start=(100, 50), end=(-50, 50), width=1, coordinate="scale", clip=True, x_clip=False, y_clip=True)
    l = pt.line(start=(100, 50), end=(-50, 50), color='red', width=1, coordinate="scale", clip=True)
    l = pt.line(start=(130, 80), end=(130, -50), width=1, coordinate="scale", clip=True, x_clip=True, y_clip=False)
    l = pt.line(start=(130, 80), end=(130, -50), color='red', width=1, coordinate="scale", clip=True)

    l = pt.line(start=(100, 0), end=(100, -50), width=1, coordinate="scale", clip=True, x_clip=True, y_clip=False)
    l = pt.line(start=(100, 0), end=(100, -50), color='red', width=1, coordinate="scale", clip=True)

    l = pt.line(start=(-10, 0), end=(-10, -50), width=1, coordinate="scale", clip=True, x_clip=True, y_clip=False)
    l = pt.line(start=(-10, 0), end=(-10, -50), color='red', width=1, coordinate="scale", clip=True)

    # # print(l._start)
    # # add text based on coordinate scales. If the position is out of the scale, the item will be not plotted.
    # pt2.text(name="TEXT02", x=40, y=70, text="AaBbCcDdEeFfGg", size=12, font="Arial", coordinate="scale")
    # # z_index is used to move it to the top, otherwise they will be plotted based on the sequene of generation,
    # # and the former shapes will be overlapped by the latters.
    # pt3.text(name="TEXT03", x=40, y=70, text="This is the first plot area, which has a <red>z-index</red> of 999.", size=12,
    #          coordinate="scale", z_index=999)
    #
    # # plot lines and scattersW
    # for i in range(10):
    #     pt3.line(name=f"LINE_{i}", start=[0, i * 10], end=[300, i * 10 + 50], width=1, color="grey", line_style="solid")
    #
    # xs = np.random.randint(low=0, high=200, size=10)
    # ys = np.random.randint(low=0, high=200, size=10)
    #
    # # name attribute is not mandatory, but they are recommaned for finding they easier.
    # for x, y in zip(xs, ys):
    #     pt.scatter(name=f"SCATTER_{x}_{y}", x=x, y=y, size=2, coordinate="scale", fill_color="red" if y <= 100 else "grey")
    #
    # # eight line styles are supported currently, namely:
    # #    "solid" "dotted" "dashed" "dashdot" "densely_dashed" "loosely_dashed" "densely_dotted" "loosely_dotted"
    # for x in range(0, 200, 50):
    #     pt.line(name=f"LINE_X_{x}", start=[x, 0], end=[x, 300], width=1, color="grey", line_style="dashed")
    #     pt2.line(name=f"LINE_X_{x}", start=[x, 0], end=[x, 300], width=1, color="grey", line_style="dashed")
    #
    # for y in range(0, 200, 50):
    #     pt.line(name=f"LINE_Y_{y}", start=[0, y], end=[300, y], width=1, color="grey", line_style="dashdot")
    #     pt2.line(name=f"LINE_Y_{y}", start=[0, y], end=[300, y], width=1, color="grey", line_style="dashdot")
    #
    # # Finally we need to add canvas to a page
    # # As default, the page index starts from 1 because it is more intuitional. It can be defined as base = 0
    file.canvas(page=1, margin_left=1, margin_top=10, canvas=cv, unit="cm")
    file.canvas(page=2, margin_left=1, margin_top=10, canvas=cv, unit="cm")

    # add text to page instead of a canvas, in this case the position will be in pixel
    # <r> for break, <sup> and <sub> for superscript and subscript respectively.
    # file.text(page=0, x=200, y=700, line_space=1.2, text=f"Hello World!    <r><sup>=</sup>o<sup>=</sup>", size=36, base=0)

    # save pdf
    file.save()


def case2():

    # open ararpy files
    file_path = r'D:\PythonProjects\pdf-maker\venv\Lib\site-packages\ararpy\examples\22WHA0433.arr'
    sample = ap.from_arr(file_path=file_path)

    plot: ap.Plot = sample.InvIsochronPlot

    xaxis: ap.Axis = plot.xaxis
    yaxis: ap.Axis = plot.yaxis
    set1: ap.Set = plot.set1
    set2: ap.Set = plot.set2
    age_results = sample.Info.results.isochron["figure_3"]

    plot_scale = (xaxis.min, xaxis.max, yaxis.min, yaxis.max)

    # create a canvas
    cv = pm.Canvas(width=17, height=12, unit="cm", show_frame=True, clip_outside_plot_areas=False)
    # change frame outline style
    cv.show_frame(color="grey", line_width=0.5)
    pt = cv.add_plot_area(name="Plot1", plot_area=(0.15, 0.15, 0.8, 0.8), plot_scale=plot_scale, show_frame=True)

    # isochron scatters
    data = ap.calc.arr.transpose(plot.data)
    for (x, sx, y, sy, r, i) in data:
        pt.scatter(x, y, fill_color="red" if (i-1) in set1.data else "blue" if (i-1) in set2.data else "white", size=2)

    # isochron line
    line1: list = plot.line1.data
    pt.line(start=line1[0], end=line1[1], clip=True, width=1, color='red')

    # split sticks
    xaxis.interval = (xaxis.max - xaxis.min) / xaxis.split_number
    yaxis.interval = (yaxis.max - yaxis.min) / yaxis.split_number
    for i in range(xaxis.split_number + 1):
        start = pt.scale_to_points(*(xaxis.min + xaxis.interval * i, yaxis.min))
        end = pt.scale_to_points(xaxis.min + xaxis.interval * i, yaxis.min)
        end = (end[0], start[1] - 5)
        pt.line(start=start, end=end, width=1, line_style="solid", clip=False, coordinate="pt")
        pt.text(x=start[0], y=end[1] - 15, text=f"{xaxis.min + xaxis.interval * i}", clip=False,
                coordinate="pt", h_align="middle")
    for i in range(yaxis.split_number + 1):
        start = pt.scale_to_points(*(xaxis.min, yaxis.min + yaxis.interval * i))
        end = pt.scale_to_points(xaxis.min, yaxis.min + yaxis.interval * i)
        end = (start[0] - 5, end[1])
        pt.line(start=start, end=end, width=1, line_style="solid", clip=False, coordinate="pt")
        pt.text(x=end[0] - 5, y=end[1], text=f"{yaxis.min + yaxis.interval * i}", clip=False,
                coordinate="pt", h_align="right", v_align="center")

    # axis titles
    p = pt.scale_to_points((xaxis.max + xaxis.min) / 2,  yaxis.min)
    pt.text(x=p[0], y=p[1] - 30, text=f"<sup>39</sup>Ar<sub>K</sub>/<sup>40</sup>Ar*",
            clip=False, coordinate="pt", h_align="middle", v_align="top")
    p = pt.scale_to_points(xaxis.min, (yaxis.max + yaxis.min) / 2)
    pt.text(x=p[0] - 50, y=p[1], text=f"<sup>36</sup>Ar<sub>a</sub>/<sup>40</sup>Ar*",
            clip=False, coordinate="pt", h_align="middle", v_align="bottom", rotate=90)

    # inside text
    age, sage = round(age_results[0]['age'], 2), round(age_results[0]['s2'], 2)
    F, sF = round(age_results[0]['F'], 2), round(age_results[0]['sF'], 2)
    R0, sR0 = round(age_results[0]['initial'], 2), round(age_results[0]['sinitial'], 2)
    pt.text(x=(xaxis.max - xaxis.min) * 0.6 + xaxis.min,
            y=(yaxis.max - yaxis.min) * 0.7 + yaxis.min,
            text=f"Age ={age} {chr(0xb1)} {sage} Ma<r>F = {F} {chr(0xb1)} {sF}<r>"
                 f"R<sub>0</sub> = {R0} {chr(0xb1)} {sR0}",
            clip=True, coordinate="scale", h_align="middle", v_align="center", rotate=0)

    file = pm.NewPDF(filepath="case2.pdf")
    # as default, an empty pdf will have no page
    file.add_page()
    # rich text tags should follow this priority: color > script > break
    file.text(page=0, x=300, y=780, line_space=1.2, size=24, base=0, h_align="middle",
              text=f"This is a demo of creating pdf with <red>PDF-Maker</red>."
                   f"<r><sup>40</sup>Ar/<sup>39</sup>Ar Inverse Isochron")

    file.canvas(page=1, margin_top=7, canvas=cv, unit="cm", h_align="middle")

    # save pdf
    file.save()


def test_rotate():
    file = pm.NewPDF(filepath="test-subset.pdf")

    file.text(page=0, x=200, y=700, line_space=1, size=12, base=0, rotate=0, h_align="left", v_align="center",
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=200, y=725, line_space=1, size=12, base=0, rotate=0, h_align="middle", v_align="center",
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=200, y=750, line_space=1, size=12, base=0, rotate=0, h_align="right", v_align="center",
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=300, y=400, line_space=1, size=12, base=0, rotate=30, h_align="middle", v_align="center",
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=300, y=400, line_space=1, size=12, base=0, rotate=60, h_align="middle", v_align="center",
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=300, y=400, line_space=1, size=12, base=0, rotate=90, h_align="middle", v_align="center",
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=300, y=400, line_space=1, size=12, base=0, rotate=120, h_align="middle", v_align="center",
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=100, y=400, line_space=1, size=12, base=0, rotate=30,
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=100, y=400, line_space=1, size=12, base=0, rotate=60,
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=100, y=400, line_space=1, size=12, base=0, rotate=90,
              text=f"Inverse Isochron MMM")

    file.text(page=0, x=100, y=400, line_space=1, size=12, base=0, rotate=120,
              text=f"Inverse Isochron MMM")

    for i in range(6):
        file.line(page=1, start=(i*100, 0), end=(i*100, 860), width=0.5)

    for i in range(9):
        file.line(page=1, start=(0, i*100), end=(595, i*100), width=0.5)

    # save pdf
    file.save()

    # print(file.content_str)


def case1():
    basefont = "ArialMT"
    file = pm.NewPDF(filepath="case1.pdf", _basefont=basefont)
    color = "red"
    # the below two texts will use default basefont of the page, which is ArialMT
    file.text(page=0, x=20, y=100, line_space=1, size=12, base=0, rotate=0, color=color,
              h_align="left", v_align="bottom", text=f"=±=+><123456 {chr(0xb1)}  {chr(0x007B)} {chr(0x0040)} {chr(0x2264)} {chr(0x2265)} {chr(0x007D)} Test Font Embeding")
    color = '#e2dacd'
    file.text(page=0, x=20, y=150, line_space=1, size=24, base=0, rotate=0, color=color,
              h_align="left", v_align="bottom", text=f"453.45 {chr(0xb1)} 3.4 Ma Test Font Embeding")

    font_obj = file.add_font(name="Calibri", width_scale=0.5, embed=True)
    color = '#935d68'
    file.text(page=0, x=20, y=200, line_space=1, size=12, base=0, rotate=0, font=font_obj._basefont, color=color,
              h_align="left", v_align="bottom", text=f"123456 {chr(0xb1)} Test Font Embeding")

    file.text(page=0, x=20, y=250, line_space=1, size=24, base=0, rotate=0, font=font_obj._basefont,
              h_align="left", v_align="bottom", text="123456 ± Test Font Embeding")

    font_obj = file.add_font(name="MicrosoftSansSerif", width_scale=0.5, embed=True)

    file.text(page=0, x=120, y=500, line_space=1, size=12, base=0, rotate=0, font=font_obj._basefont,
          h_align="left", v_align="center", text="This is a rotated text")

    file.text(page=0, x=120, y=500, line_space=1, size=12, base=0, rotate=30, font=font_obj._basefont,
          h_align="left", v_align="center", text="This is a rotated text")

    file.text(page=0, x=120, y=500, line_space=1, size=12, base=0, rotate=60, font=font_obj._basefont,
          h_align="left", v_align="center", text="This is a rotated text")

    file.text(page=0, x=120, y=500, line_space=1, size=12, base=0, rotate=90, font=font_obj._basefont,
          h_align="left", v_align="center", text="This is a rotated text")

    file.text(page=0, x=120, y=500, line_space=1, size=12, base=0, rotate=120, font=font_obj._basefont,
          h_align="left", v_align="center", text="This is a rotated text")

    font_obj = file.add_font(name="TimesNewRomanPSMT", width_scale=0.5, embed=True)

    file.text(page=0, x=300, y=500, line_space=1, size=12, base=0, rotate=0, font=font_obj._basefont,
          h_align="middle", v_align="center", text="This is a rotated text")

    file.text(page=0, x=300, y=500, line_space=1, size=12, base=0, rotate=30, font=font_obj._basefont,
          h_align="middle", v_align="center", text="This is a rotated text")

    file.text(page=0, x=300, y=500, line_space=1, size=12, base=0, rotate=60, font=font_obj._basefont,
          h_align="middle", v_align="center", text="This is a rotated text")

    file.text(page=0, x=300, y=500, line_space=1, size=12, base=0, rotate=90, font=font_obj._basefont,
          h_align="middle", v_align="center", text="This is a rotated text")

    file.text(page=0, x=300, y=500, line_space=1, size=12, base=0, rotate=120, font=font_obj._basefont,
          h_align="middle", v_align="center", text="This is a rotated text")

    # save pdf
    file.save()


if __name__ == "__main__":
    # case2()
    # test_rotate()
    # case1()
    test_create_a_pdf()
    pass
