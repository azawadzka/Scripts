### Select pages from pdf
Open up the pdf in preview and then on the view menu select thumbnails. Ctrl select the pages that you want now drag and drop them to the desktop.

## sips 
sips (Scriptable Image Processing System) tool is a command-line utility included with macOS that allows you to perform various image manipulations:
- Format Conversion
- Resizing
- Rotating
- Batch Processing

The sips tool in macOS uses the Core Graphics framework (also known as Quartz) under the hood, apparently efficient and robust.

Convert svg to png:

```sips -s format png -o output.png input.svg```

Resize imgs to 800 px width:

```for file in *.jpg; do sips -Z 800 "$file" --out resized/"$file"; done```