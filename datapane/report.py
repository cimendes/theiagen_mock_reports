import altair as alt
import datapane as dp
import pandas as pd

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

mlst_table = pd.DataFrame({"Schema": [mlst_scheme], "ST": [mlst_st], "Profile": [mlst_profile]})

amr_table = pd.DataFrame({"Antimicrobials": [amr_classes], "AMR Genes": [amr_genes]})


view = dp.Blocks(
    dp.Text("# TheiaProk Report"),
    dp.Table(sample_table),
    dp.Table(mlst_table),
    dp.Table(amr_table)
)

dp.save_report(view, path="datapane_report.html")
