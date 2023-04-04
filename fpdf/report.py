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

sample_table = pd.DataFrame({"Sample": [sample], "Taxon ID": [taxon]})

mlst_table = pd.DataFrame({"ST": [mlst_st], "Profile": [mlst_profile]})

amr_table = pd.DataFrame({"Antimicrobials": [amr_classes], "AMR Genes": [amr_genes]})


# cell height
ch = 8

class PDF(FPDF):
    def __init__(self):
        super().__init__()
    def header(self):
        self.set_font('Arial', '', 12)
        self.cell(0, 8, 'Theiagen Genomics', 0, 1, 'R')
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', '', 12)
        self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')

# Generate PDF
pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 24)
pdf.cell(w=0, h=20, txt="TheiaProk Report", ln=1)

pdf.set_font('Arial', '', 16)
pdf.cell(w=30, h=ch, txt="Date: ", ln=0)
pdf.cell(w=30, h=ch, txt=str(date.today()), ln=1)

# Sample ID and Taxon
pdf.set_font('Arial', '', 16)
pdf.cell(w=40, h=ch, txt="Sample: ", ln=0)
pdf.cell(w=40, h=ch, txt=sample, ln=1)
pdf.cell(w=50, h=ch, txt="Taxon: ", ln=0)
pdf.cell(w=50, h=ch, txt=taxon, ln=1)

pdf.ln(ch)

# MLST
pdf.cell(w=70, h=10, txt="Multilocus Sequence Typing", ln=1)
pdf.cell(w=80, h=ch, txt="Scheme: ", ln=0)
pdf.cell(w=80, h=ch, txt=mlst_scheme, ln=1)

pdf.set_font('Arial', 'B', 8)
pdf.cell(80, ch, 'ST', 1, 0, 'C')
pdf.cell(80, ch, 'Profile', 1, 1, 'C')

pdf.set_font('Arial', '', 8)
for i in range(0, len(mlst_table)):
    pdf.cell(40, ch, mlst_table['ST'].iloc[i], 1, 0, 'C')   
    pdf.cell(40, ch, str(mlst_table['Profile'].iloc[i]), 1, 1, 'R')

pdf.ln(ch)

# AMR
pdf.set_font('Arial', '', 16)
pdf.cell(w=90, h=10, txt="in silico Antimicrobial Resistance Typing", ln=1)

pdf.set_font('Arial', 'B', 8)
pdf.cell(80, ch, 'Antimicrobials', 1, 0, 'C')
pdf.cell(80, ch, 'AMR Genes', 1, 1, 'C')

pdf.set_font('Arial', '', 8)
for i in range(0, len(amr_table)):
    pdf.cell(40, ch, str(amr_table['Antimicrobials'].iloc[i]), 1, 0, 'C')   
    pdf.cell(40, ch, str(amr_table['AMR Genes'].iloc[i]), 1, 1, 'R')

pdf.output(f'./fpdf_report.pdf', 'F')