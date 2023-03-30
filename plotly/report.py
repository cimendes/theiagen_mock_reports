import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

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
                        [{"type": "table", "rowspan": 2, "colspan": 1}, None, None],
                        [None, None, None],
                        [{"type": "table", "rowspan": 2, "colspan": 3}, None, None],
                        [None, None, None],
                        [{"type": "table", "rowspan": 2, "colspan": 3}, None, None],
                        [None, None, None]],
                    subplot_titles=("","Summary Table", "MLST", "Hits Table"))

 # intro text
summary = ('Add blirp about <a href="https://github.com/theiagen/public_health_bacterial_genomics/">TheiaProk</a> here.<br> '
            ' <br>'
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec feugiat sodales cursus.'
            'Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.'
            'Etiam pulvinar pretium posuere.'
            ' <br>')

fig.add_annotation(x=0, xref='paper', y=1, yref='paper', text=summary,
                       showarrow=False, font=dict(size=14), align='center', 
                       bgcolor='#f0f0f0')

 # summary table
fig.add_trace(go.Table(header=dict(values=["Sample", "Taxon ID"],
                        font=dict(size=14, color="white"), align="center", fill_color="#196db5"),
                        cells=dict(values=[sample, taxon], align = ["left", "center"], fill_color='#f0f0f0')),
                row=3, col=1)

# mlst table
fig.add_trace(go.Table(header=dict(values=["Schema", "ST", "Profile"],
                        font=dict(size=14, color="white"), align="center", fill_color="#196db5"),
                        cells=dict(values=[mlst_scheme, mlst_st, mlst_profile], align = ["left", "center"], fill_color='#f0f0f0')),
                row=5, col=1)

# mlst table
fig.add_trace(go.Table(header=dict(values=["Antimicrobials", "AMR Genes"],
                        font=dict(size=14, color="white"), align="center", fill_color="#196db5"),
                        cells=dict(values=[amr_classes, amr_genes], align = ["left", "center"], fill_color='#f0f0f0')),
                row=7, col=1)

# title
fig.update_layout(title={'text': "<b>TheiaProk Report</b>",
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'size': 24, 'color': '#196db5'}})
fig.update_layout(height=1080, template='ggplot2', plot_bgcolor='rgba(0,0,0,0)')
fig.write_html("plotly_report.html", include_plotlyjs="cdn")