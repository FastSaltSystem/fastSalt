"""Render the preserved report; does not run any engineering calculations."""
from pathlib import Path
import os, re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
D=Path(__file__).resolve().parent
F=Path(os.environ.get('STUDY_FONT_DIR','/usr/share/fonts/truetype/dejavu'))
pdfmetrics.registerFont(TTFont('Study',str(F/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('StudyBold',str(F/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Study',normal='Study',bold='StudyBold',italic='Study',boldItalic='StudyBold')
style={
'p':ParagraphStyle('body',fontName='Study',fontSize=9.5,leading=13.4,spaceAfter=8,textColor=colors.HexColor('#223544')),
'h1':ParagraphStyle('title',fontName='StudyBold',fontSize=22,leading=27,spaceAfter=16,textColor=colors.HexColor('#173c51')),
'h2':ParagraphStyle('section',fontName='StudyBold',fontSize=12,leading=16,spaceBefore=10,spaceAfter=7,keepWithNext=True,textColor=colors.HexColor('#173c51')),
'cell':ParagraphStyle('cell',fontName='Study',fontSize=8.0,leading=10.8,textColor=colors.HexColor('#223544')),
}
def inline(s):
 s=html.escape(s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2" color="#17678c">\1</a>',s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'`([^`]+)`',r'<font name="Study">\1</font>',s)
 return s
blocks=[];web=[];lines=(D/'report.md').read_text().splitlines();i=0
while i<len(lines):
 l=lines[i];i+=1
 if not l.strip():continue
 if l=='<!-- pagebreak -->':blocks.append(PageBreak());web.append('<hr class="pagebreak">');continue
 if l.startswith('# '):s=l[2:];blocks.append(Paragraph(inline(s),style['h1']));web.append('<h1>'+inline(s)+'</h1>');continue
 if l.startswith('## '):s=l[3:];blocks.append(Paragraph(inline(s),style['h2']));web.append('<h2>'+inline(s)+'</h2>');continue
 if l.startswith('|'):
  rows=[l]
  while i<len(lines) and lines[i].startswith('|'):rows.append(lines[i]);i+=1
  rows=[r for r in rows if not re.fullmatch(r'[| :\-]+',r)]
  data=[[c.strip() for c in r.strip('|').split('|')] for r in rows]
  n=len(data[0]);widths={5:[182,82,82,82,82],3:[160,185,165],4:[60,105,235,110]}[n]
  cells=[[Paragraph(('<b>'+inline(c)+'</b>') if j==0 else inline(c),style['cell']) for c in row] for j,row in enumerate(data)]
  t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce9f0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f8')]),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c9d4dc')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]))
  blocks+=[t,Spacer(1,10)]
  web.append('<div class="tablewrap"><table>'+''.join('<tr>'+''.join(('<th>' if j==0 else '<td>')+inline(c)+('</th>' if j==0 else '</td>') for c in row)+'</tr>' for j,row in enumerate(data))+'</table></div>');continue
 if l.startswith('- '):
  blocks.append(Paragraph(inline(l[2:]),style['p'],bulletText='•'));web.append('<p class="bullet">• '+inline(l[2:])+'</p>');continue
 while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','- ','<!--')):l+=' '+lines[i];i+=1
 blocks.append(Paragraph(inline(l),style['p']));web.append('<p>'+inline(l)+'</p>')
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#c9d4dc'));canvas.line(43,45,553,45)
 canvas.setFont('Study',8);canvas.setFillColor(colors.HexColor('#536d7d'));canvas.drawString(43,31,'FAST SALT SYSTEM  |  RS-008  |  Revision A  |  19 October 2026');canvas.drawRightString(553,31,str(doc.page));canvas.restoreState()
SimpleDocTemplate(str(D/'report.pdf'),pagesize=(596,842),leftMargin=43,rightMargin=43,topMargin=39,bottomMargin=59,title='Auxiliary Brayton Cooling Options for the Fast Salt System - Revision A',author='Fast Salt System project',pageCompression=1).build(blocks,onFirstPage=footer,onLaterPages=footer)
css='body{margin:0;background:#f1f5f7;color:#223544;font:17px/1.6 system-ui,sans-serif}main{max-width:1120px;margin:30px auto;padding:36px;background:white}h1,h2{color:#173c51;line-height:1.25}h2{margin-top:1.7em}a{color:#17678c}table{width:100%;border-collapse:collapse;font-size:15px}td,th{border:1px solid #c9d4dc;padding:10px;text-align:left;vertical-align:top}th{background:#dce9f0}tr:nth-child(even){background:#f3f6f8}.tablewrap{overflow-x:auto}.pagebreak{border:0;border-top:1px solid #c9d4dc;margin:35px 0}.bullet{padding-left:1em}@media print{.pagebreak{break-before:page}main{margin:0;padding:0}}'
(D/'report.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RS-008 | Auxiliary Brayton Cooling Options | Revision A</title><style>'+css+'</style></head><body><main><p><a href="report.pdf">Download PDF</a> · <a href="README.md">Study record</a></p>'+''.join(web)+'</main></body></html>')
print('Rendered report.pdf and report.html from report.md')
