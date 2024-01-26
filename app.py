import streamlit as st
import pandas as pd
import numpy as np

import ast
from io import StringIO
import codecs

from mmconverter.utils import *

st.title("Convertisseur de requêtes Crésus")

uploaded_file = st.file_uploader(label = "Ajouter une requête Crésus")


def tryeval(val):
    try:
        val = ast.literal_eval(val)
    except ValueError:
        pass
    return val


if uploaded_file:

    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(bytes_data.decode("ANSI"))
    string_data = stringio.read()
    rows = string_data.replace('"', '').split("\r")
    rows = [row.split(";") for row in rows]
    # st.write(rows)

    df = process_rows(rows)
    st.dataframe(df)

    csv = df.to_csv(sep = ";", index = False)
    st.download_button(
        label = "Télécharger la requête convertie",
        data = csv,
        file_name = f"{uploaded_file.name[:-4]}_converted.csv",
        mime = "text/csv"
        )


