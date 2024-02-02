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

save_filepath = r"D:\PythonProjects\pdf-tool\default.pdf"
a = pt.NewPDF(filepath=save_filepath)
a.set_page_size(index=0, width=1000, height=1000)


stream = pt.Obj(type="", index="6", text=[pt.Text(
    font_name="F1", font="arial", size=24, x=100, y=100, text="This is the second page")])
page = pt.Obj(type="page", index="7", parent="2", contents="6", mediabox=[0, 0, 1000, 300])
a.add_obj(obj=stream)
a.add_obj(obj=page)

a.add_page(size=[500, 500])

a.text(page=0, x=100, y=100, line_space=2,
       text=f"Test <sup>40</sup>Ar<sub>K</sub>\n<r>Test<red>Test</red>", size=24)
a.line(page=0, start=[200, 200], end=[400, 400], width=1, color="black")
a.line(page=0, start=[600, 200], end=[400, 400], width=5, color="red")
a.rect(page=0, left_bottom=[200, 200], width=400, height=400, line_width=1, color="blue")

a.del_obj(index=7)
a.del_obj(index=a.get_page_indexes()[-1])

a.save()
print(a.content_str)

