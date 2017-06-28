#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET

xmlFileName = 'out.xml'
outFileName = 'result.html'
xmlText = ET.parse(xmlFileName);
htmlDocText = '''<!DOCTYPE html>
<html>
<head>
{style}
<title>HTML report from catch</title>
</head>
<body>
{contents}
</body>
</html>'''

def getThStyle(tag):
    style = ''
    if tag == 'Group':
        style = 'class=group'
    elif tag == 'TestCase':
        style = 'class=testcase'
    elif tag == 'OverallResult':
        style = 'class=overallresult'
    elif tag == 'OverallResults':
        style = 'class=overallresults'
    return style

def getTdHTML(key, val):
    html = '<td><b>'+key+'</b></td>'+'<td {style}>'+val+'</td>'
    style_=''
    if key == "success":
        if val == "true":
            style_='style="color: blue;"'
        else:
            style_='style="color: red; font-weight:bold;"'
    elif key == "failures" and val > 0:
        style_='style="color: red; font-weight:bold;"'
    html = html.format(style=style_)
    return html

def convertToHTML(node):
    html='<table style="width:100%"><th '+getThStyle(node.tag)+' colspan="'+\
    str(len(node.keys())*2)+'">'+node.tag+'</th>{rows}</table>'
    tds = ''
    for key in node.keys():
        tds+=getTdHTML(key, node.attrib[key])
    html = html.format(rows = '<tr>'+tds+'</tr>{rows}')
    tds = ''
    if type(node.text) is str:
        text = node.text.strip()
        if text != "":
            tds += '<td colspan="'+str(len(node.keys())*2)+'">'+\
            node.text.strip()+'</td>'
    html = html.format(rows = tds)
    return html

def xmlIter(root):
    html = ''
    for node in root:
        html += convertToHTML(node)
        html += xmlIter(node)
    return html

# Set style
cssStyle = '''<style>
table, th, td {border: 1px solid black;border-collapse: collapse;}
th, td {padding: 5px;text-align: left;}
th.group {background-color: #00131a; color: white;}
th.testcase {background-color: yellow;}
th.overallresult {background-color: #80ff80;}
th.overallresults {background-color: #8080ff;}
th {background-color: #ffffcc;}
</style>'''

# Convert xml to html
root = xmlText.getroot()
htmlDocText = htmlDocText.format(style = cssStyle, contents = xmlIter(root))

# Output {outFileName}.html
f = open(outFileName, "w")
f.write(htmlDocText);
f.close();
