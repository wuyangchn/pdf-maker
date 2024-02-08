通常，创建的PDF文件具有如下结构：

    %PDF-1.7
    1 0 obj

    <<
    /Type /Catalog
    /Pages 2 0 R
    >>
    endobj
    2 0 obj
    
    <<
    /Type /Pages
    /Kids [10 0 R]
    /Count 1
    >>
    endobj
    3 0 obj
    
    <<
    /Type /Font
    /Subtype /TrueType 
    /Name /F1 
    /FirstChar 0 
    /LastChar 255 
    /Widths [...]
    /BaseFont /Arial 
    /Encoding 4 0 R
    /FontDescriptor 5 0 R
    >>
    endobj
    4 0 obj
    
    <<
    /Type /Encoding
    /Differences
    []
    >>
    endobj
    5 0 obj
    
    <<
    /Type /FontDescriptor
    /FontBBox [-1361 -665 4096 2129]
    /FontFile2 6 0 R
    /FontName /Arial 
    /Flags 00001000 00011011 
    /Ascent 1854 
    /Descent -434 
    /CapHeight 1467 
    /ItalicAngle 0 
    /StemV 95 
    /MissingWidth 452 
    >>
    endobj
    6 0 obj
    
    <<
    /Filter /ASCIIHexDecode 
    /Length 0
    /Length1 0
      
      
    >>
    stream
    
    endstream
    endobj
    7 0 obj
    
    <<
    /Title (NewPDF)
    /CreationDate (D:20240208220342651971+08'00')
    /ModDate (D:20240208220342651971+08'00')
    >>
    endobj
    8 0 obj

    <<
    /Length 9 0 R 
    >>
    stream
    endstream
    endobj
    9 0 obj
    16258
    <<
    >>
    endobj
    10 0 obj
    
    <<
    /Type /Page
    /Parent 2 0 R
    /MediaBox [0 0 595 842]
    /Contents 8 0 R
    /Resources <<
    /Procset [/PDF /Text]
    /Font <<
    /F1 3 0 R
    >>
    >> 
    >>
    endobj
    
其结构可以表示为：
    page [2 0 R] -> Font [3 0 R] -> FontDescriptor [5 0 R]
    
示例中字体文件并没有插入到 FontDescriptor。如果要嵌入字体文件，需要在 FontDescriptor 中加入可选字典 FontFile，根据字体类型不同
有FontFile, FontFile2, 和 FontFile3 三种键值。

StackOverflow 上有大佬分享了嵌入字体的形式。

https://stackoverflow.com/questions/76123231/placing-a-subset-of-a-font-into-a-manually-created-pdf/76125971#76125971

赋值他提供的pdf编码，Adobe Acrobat成功识别了嵌入的字体。

这其中的难点是从一个完整的文件中拆分部分字符组成的子集，但如果不在乎文件大小，直接全部嵌入字体文件呢？

下面是一个尝试：直接打开ttf字体文件，将二进制字符转为16进制值后写入stream对象，但最终Adobe Acrobat并不能识别。
        
    file = "arial.ttf"
    font_file_bytes = open(file, 'rb').read()
    font_file_hex = font_file_bytes.hex() + ">"
    # 将font_file_hex加入后pdf如下：
    
    5 0 obj
    
    <<
    /Type /FontDescriptor
    /FontBBox [-1361 -665 4096 2129]
    /FontFile2 6 0 R
    /FontName /Arial 
    /Flags 00001000 00011011 
    /Ascent 1854 
    /Descent -434 
    /CapHeight 1467 
    /ItalicAngle 0 
    /StemV 95 
    /MissingWidth 452 
    >>
    endobj
    6 0 obj
    
    <<
    /Filter /ASCIIHexDecode 
    /Length 2112840
    /Length1 1045960
    >>
    stream
    00010000001901000004009044534947c490cf46000fd444000021844744454618e61c66000d34800000035847504f533211
    17c5000d37d80002181447535542b2846bb8000f4fec000083d84a5354466d2a6906000fd3c40000001e4c5453482a36e5d5
    ...............>
    endstream
    endobj
    
查找失败的原因：

Kurt介绍了从PDF中提取字体信息的方法。

https://stackoverflow.com/questions/76123231/placing-a-subset-of-a-font-into-a-manually-created-pdf/76125971#76125971

因此，首先尝试从我们创建的pdf中获取字体信息，判断字体文件是否正确写入pdf。

利用 pdf-parser.py 提取font file stream
    
    python pdf-parser.py -s mypdf.pdf  # 读取pdf结构
    python pdf-parser.py -o 6 -d dumped-data.ext new.pdf  # 6是font file stream的obj 索引， 生成dumped data (16进制)
    python pdf-parser.py -o 6 -f -d dumped-decoded-data.ext new.pdf  # 6是font file stream的obj 索引，生成decoded data 
    利用 file tofinfo 可以查看dumped-decoded-data.ext中的字体信息
    file和tofinfo需要安装TeX Live使用



    


    