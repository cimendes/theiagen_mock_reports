import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots
from datetime import date

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

# main report skeleton 
fig = make_subplots(rows=8, cols=3, vertical_spacing=0.1, 
                specs=[[None, {"type": "table", "rowspan": 1, "colspan": 2}, None],
                        [None, None, None],
                        [{"type": "table", "rowspan": 2, "colspan": 3}, None, None],
                        [None, None, None],
                        [{"type": "table", "rowspan": 2, "colspan": 3}, None, None],
                        [None, None, None],
                        [{"type": "table", "rowspan": 2, "colspan": 3}, None, None],
                        [None, None, None]],
                    subplot_titles=("","", "", ""))

# define size as A4 in pixels for PDF generation
# https://www.papersizes.org/a-sizes-in-pixels.htm
fig.update_layout(
    autosize=False,
    width=1240,
    height=1754,
    template='ggplot2', plot_bgcolor='rgba(0,0,0,0)'
)

# Add Theiagen Logo
fig.add_layout_image(
    dict(
        source="https://i.imgur.com/39cSdKS.png",
        xref="paper", yref="paper",
        x=1, y=1,
        sizex=0.2, sizey=0.2,
        xanchor="right", yanchor="bottom"
    )
)

# Title
fig.update_layout(title={'text': "<b>TheiaProk Report</b>",
                        'y':0.90,
                        'x':0.2,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'size': 34, 'color': '#196db5'}})

 # Intro and Taxon Identification
fig.add_annotation(x=0, xref='paper', y=0.89, yref='paper', text=f"<b>Sample:</b> {sample}",
                       showarrow=False, font=dict(size=18), align='left', 
                       bgcolor='white')

fig.add_annotation(x=0, xref='paper', y=0.87, yref='paper', text=f"<b>Date:</b> {str(date.today())}",
                       showarrow=False, font=dict(size=18), align='left', 
                       bgcolor='white')

fig.add_annotation(x=0, xref='paper', y=0.85, yref='paper', text=f"<b>Taxon:</b> <i>{taxon}</i>",
                       showarrow=False, font=dict(size=18), align='left', 
                       bgcolor='white')

# MLST Results
fig.add_annotation(x=0, xref='paper', y=0.80, yref='paper', text=f"<b>Multilocus Sequence Typing</b>",
                       showarrow=False, font=dict(size=24, color='white'), align='left', 
                       bgcolor='#196db5')
fig.add_annotation(x=0, xref='paper', y=0.76, yref='paper', text=f"<b>Scheme:</b> <i>{mlst_scheme}</i>",
                       showarrow=False, font=dict(size=18), align='left', 
                       bgcolor='white')
fig.add_trace(go.Table(columnorder = [1,2],
                       columnwidth = [80,400],
                       header=dict(values=["<b>ST</b>", "<b>Profile</b>"],font=dict(size=18, color="white"), align="center", fill_color="#196db5"),
                       cells=dict(values=[mlst_st, mlst_profile], align = ["center", "left"], fill_color='#f0f0f0', font=dict(size=16))),
                row=3, col=1)

# AMR Results
fig.add_annotation(x=0, xref='paper', y=0.60, yref='paper', text=f"<b>Antimicrobial Resistance <i>in silico</i> Typing</b>",
                       showarrow=False, font=dict(size=24, color='white'), align='left', 
                       bgcolor='#196db5')


summary = ('This report has been generated with <a href="https://github.com/theiagen/public_health_bacterial_genomics/">TheiaProk</a>.')


fig.write_image("plotly_report.pdf")