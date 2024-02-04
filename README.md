# PDF-Maker
A module for creating PDF files manually.

## Example usage:

### Create a simple PDF with Hello World!
    
    import pdf_maker as pm
    
    file = pt.NewPDF(filepath="myPDF.pdf")
    
    # write text to the given page
    file.text(page=0, x=300, y=600, line_space=2,
       text=f"Hello <red>World</red>!", size=36)
    
    file.save()
    
### Add pages

    import pdf_maker as pm
    
    file = pt.NewPDF(filepath="myPDF.pdf")
    
    print(file.get_page_indexes())
    
    file.set_page_size(index=0, width=1000, height=1000)
    
    file.add_page(size=(500, 500))
    
    new_page_content = pt.Obj(index="9", type="Stream")
    file.add_obj(obj=new_page_content)
    
    page_parent = file.get_obj(type="Pages")[0]
    page_font = file.get_obj(type="Font")[0]
    file.add_obj(index="10", type="Page", contents="9", parent=page_parent.index(), mediabox=[0, 0, 400, 800],
                 resources=pt.Resources(font=page_font.get_font_name(), font_index=page_font.index()))
    
    print(file.get_page_indexes())
    
    file.text(page=1, x=200, y=600, line_space=2,
              text=f"This is the <red>first</red> page.", size=36)
    file.text(page=2, x=200, y=200, line_space=2,
              text=f"This is the <blue>second</blue> page.", size=24)
    file.text(page=3, x=200, y=500, line_space=2,
              text=f"This is the 3<sup>th</sup> page.<r>New line.", size=24)
    
    file.move_page(from_index=1, to_index=3, base=1)
    
    file.save()

### Draw scatters and lines
    
    import pdf_maker as pm
    
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
    
