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

stream = pt.Obj(type="", index="6", text=[{
            "Tf": {"name": "", "index": "", "size": "24"},
            "Td": {"x": "100", "y": "100"},
            "Tj": {"text": "This is the second page"},
        }])
page = pt.Obj(type="page", index="7", parent="2", contents="6", mediabox=[0, 0, 1000, 300])
a.add_obj(obj=stream)
a.add_obj(obj=page)

a.save()
print(a.content_str)

