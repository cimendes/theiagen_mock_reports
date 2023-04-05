import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import lorem
from datetime import date
from fpdf import FPDF

amr_classes = []
amr_genes = []
mlst_st = ''
mlst_profile = []
mlst_scheme = ''
taxon = ''
sample = ''

## Load data
with open("data/AMR_CLASSES", "r") as amr_classes_fh:
    amr_classes = amr_classes_fh.readlines()
with open("data/AMR_GENES", "r") as amr_genes_fh:
    amr_genes = amr_genes_fh.readlines()
with open("data/MLST_ST", "r") as mlst_st_fh:
    mlst_st = mlst_st_fh.read()
with open("data/MLST_PROFILE", "r") as mlst_profile_fh:
    mlst_profile = mlst_profile_fh.readlines()
with open("data/MLST_SCHEME", "r") as mlst_scheme_fh:
    mlst_scheme = mlst_scheme_fh.read()
with open("data/TAXON", "r") as taxon_fh:
    taxon = taxon_fh.read()
with open("data/SAMPLE_ID", "r") as sample_id_fh:
    sample = sample_id_fh.read()

# colour pallete
colours = ["#196db5", "#0fc173"]

class PDF(FPDF):
    def __init__(self):
        super().__init__()
    def header(self):
        # add logo to top right corner of page
        #self.image("data/logo_theiagen.png", 150, 8, 45)
        self.ln(15)
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', '', 10)
        self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')
    def create_table(self, table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None,emphasize_color=(0,0,0)): 
        """
        table_data: 
                    list of lists with first element being list of headers
        title: 
                    (Optional) title of table (optional)
        data_size: 
                    the font size of table data
        title_size: 
                    the font size fo the title of the table
        align_data: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width: 
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start: 
                    where the left edge of table should start
        emphasize_data:  
                    which data elements are to be emphasized - pass as list 
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black) 
        
        """
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style
        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4) # add 4 for padding
                col_width = col_widths



                        ### compare columns 

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int        
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else: # need to multiply cell width by number of cells to get table width 
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height) # move cursor back to the left margin

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)

            for row in data:
                if x_start: # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left,y3,x_right,y3)

# Generate PDF
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
ch=12 # default font size
pdf.set_font('helvetica', '', ch)

# Add page
pdf.add_page()
pdf.set_font('Helvetica', 'B', 24)
pdf.cell(w=0, h=20, txt="TheiaProk Report", ln=1)
#pdf.image("data/logo_theiagen.png", 150, 8, 45)

pdf.set_font('Arial', '', 16)
pdf.cell(w=30, h=ch, txt="Date: ", ln=0)
pdf.cell(w=30, h=ch, txt=str(date.today()), ln=1)

# Sample ID and Taxon
pdf.set_font('Arial', '', 16)
pdf.cell(w=30, h=ch, txt="Sample: ", ln=0)
pdf.cell(w=30, h=ch, txt=sample, ln=1)
pdf.cell(w=30, h=ch, txt="Taxon: ", ln=0)
pdf.cell(w=30, h=ch, txt=taxon, ln=1)

pdf.ln(ch)

# MLST Table
pdf.cell(w=70, h=10, txt="Multilocus Sequence Typing", ln=1)
pdf.cell(w=80, h=ch, txt="Scheme: ", ln=0)
pdf.cell(w=80, h=ch, txt=mlst_scheme, ln=1)

mlst_data = [['ST', 'Profile'], [mlst_st, mlst_profile]]
pdf.create_table(table_data=mlst_data, title='', cell_width=[15,150], x_start=10)
pdf.ln(ch)

# AMR
pdf.set_font('Arial', '', 16)
pdf.cell(w=90, h=10, txt="in silico Antimicrobial Resistance Typing", ln=1)

amr_data_1 = [['Antimicrobials'], [','.join(amr_classes)]]
pdf.create_table(table_data=amr_data_1, title='', cell_width=[165], x_start=10)
pdf.ln(ch)

amr_data_2 = [['AMR genes'], [','.join(amr_genes)]]
pdf.create_table(table_data=amr_data_2, title='', cell_width=[165], x_start=10)
pdf.ln(ch)

pdf.output(f'./fpdf_report.pdf', 'F')