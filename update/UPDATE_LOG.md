# 2024-02-10 v0.0.36
* Fix the error of embedding fonts.

Source font file size:

![alt text](image-2.png)

Extracted font file size:

![alt text](image-3.png)

There is a difference of 4 bytes. The extracted file missed four charachters. So the issue might happen during the hex encoding procedure.

![alt text](image-4.png)

Furtherly, it is noticed that the difference happens after the realignment of the hexadecimal representation, in which errors might happen.

![alt text](image-5.png)

Finally identify the issue: should be len(hex_stream) // 64 instead of that + 1.

![alt text](image-6.png)

Three fonts are all embedded.

![alt text](image-7.png)

# 2024-02-09 v0.0.35
* Add multiply fonts to pages. 
* TrueType fonts like Arial are displayed well now, but Type 1 font don't work well.
Possible reason: comparing extracted font file by pdf-parser.py from the pdf and the source file times.ttf,
it is found that extracted font file lost some information. Times ttf might be not TrueType font.

![alt text](image.png)

![alt text](image-1.png)

# 2024-02-09 v0.0.34
* Try to solve the embedding issue, some potential problems found: length calculation of the font file 
stream.
* A javascript module named [fontsubset](https://github.com/flashlizi/fontsubset) can be used to extract 
subset from a full font file so the size of pdf with embedded font files can be decreased. 
Usage: fontsubset -s "String containing characters might be included" fontFile outputFile

# 2024-02-08 v0.0.33
* Add rotation attribute for text item (might also work for other items like rect).
* Change the priorities of three rich text tags, now color > super/subscript > break. That means
<red>AB<sub>CD</sub><r>EF<red> is allowed, but AB<sub><red>CD</red></sub> will be not displayed correctly.
And these tags should not separate others, like <red><sub>CD</red></sub>, which will be displayed wrong.

# 2024-02-08 v0.0.32
* Try to embed font files into the Font Descriptor objects. 
[This answer](https://stackoverflow.com/a/76125971/22143697) show an example of embedding font files, 
his pdf works well in Adobe Acrobat. But I failed to do this, still trying to fine why.
* For reference, [This answer](https://stackoverflow.com/a/3489099/22143697) introduced how to extract
font info from a pdf file. 
* This issue haven't been solve.

# 2024-02-07 v0.0.31
* Fix font issue, currently Arial font works well, Adobe can successfully recognize the texts,
but other fonts may not work for Adobe Acrobat. Adobe Illustrator can work well for all fonts.
* Add auto middle alignment for tests.
 
# 2024-02-07 v0.0.3
* Add other attributions such as FontDescriptor in the Font object.
* Read font information from xml files, and embed them into the pdf.
* A horizontal scale (integer) will be used to control the actual widths of characters, default 0.5.

# 2024-02-05 v0.0.2
* Add canvas

# 2024-02-04  v0.0.1
* First release
* Basic functions: Create a PDF, add text, lines and scatters. Supports superscript
 and subscript and different color in one string.
