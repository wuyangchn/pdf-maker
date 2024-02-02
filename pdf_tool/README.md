# PDF-Tool
A module for creating PDF files manually.

## Example usage:
    
    import pdf_tool as pt
    
    # create instance
    save_filepath = "myPDF.pdf"
    file = pt.NewPDF(filepath=save_filepath)
    
    # set page size, in default when you create an instantce, there will be one page in the file
    file.set_page_size(index=0, width=1000, height=1000)
    
    # create a new stream obj with text
    text = pt.Text(font_name="F1", font="arial", size=24, x=100, y=100, text="This is the second page")
    stream = pt.Obj(type="", index="6", text=[text])
    
    # create new page that contains the stream
    page = pt.Obj(type="page", index="7", parent="2", contents="6", mediabox=[0, 0, 1000, 300])
    
    # add two objs
    file.add_obj(obj=stream)
    file.add_obj(obj=page)
    
    # add a new page to the end with page size of [width, height]
    file.add_page(size=[500, 500])
    
    # write text to the given page
    file.text(page=0, x=100, y=100, line_space=2,
       text=f"Test <sup>40</sup>Ar<sub>K</sub>\n<r>Test<red>Test</red>", size=24)
    
    # draw lines to the given page
    file.line(page=0, start=[200, 200], end=[400, 400], width=1, color="black")
    file.line(page=0, start=[600, 200], end=[400, 400], width=5, color="red")
    
    # draw a rectangle to the given page
    file.rect(page=0, left_bottom=[200, 200], width=400, height=400, line_width=1, color="blue")
    
    # delete a obj
    file.del_obj(index=7)
    
    # delete the last page
    file.del_obj(index=a.get_page_indexes()[-1])
    
    # save pdf
    file.save()
    
