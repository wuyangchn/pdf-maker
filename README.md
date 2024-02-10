# PDF-Maker
A module for creating PDF files manually.

## Update log

[Update log](/update/UPDATE_LOG.md)

**2024-02-10 v0.0.38**
* Fix the display error of double quotation marks, which was missed in the subset font files.

## Example usage:

*Case 1: Plot scatters and lines and write text based on a coordinate system*

view the pdf generated in this example: [pdf](tests/case1.pdf)
    
    basefont = "ArialMT"
    file = pm.NewPDF(filepath="case1.pdf", _basefont=basefont)

    # the below two texts will use default basefont of the page, which is ArialMT
    file.text(page=0, x=20, y=100, line_space=1, size=12, base=0, rotate=0,
              h_align="left", v_align="bottom", text="123456 ± Test Font Embeding")

    file.text(page=0, x=20, y=150, line_space=1, size=24, base=0, rotate=0,
              h_align="left", v_align="bottom", text="123456 ± Test Font Embeding")

    font_obj = file.add_font(name="Calibri", width_scale=0.5, embed=True)

    file.text(page=0, x=20, y=200, line_space=1, size=12, base=0, rotate=0, font=font_obj._basefont,
              h_align="left", v_align="bottom", text="123456 ± Test Font Embeding")

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


*Case 2: (v0.0.4) Plot isochron with ArArPY files*

view the pdf generated in this example: [pdf](tests/case2.pdf)

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
    