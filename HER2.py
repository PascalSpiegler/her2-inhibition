import streamlit as st
import pandas as pd
import subprocess
import os
import base64
import pickle

# Molecular descriptor calculator
def desc_calc(load_data):
    #Performs the descriptor calculation
    bashCommand = 'java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv'
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('molecule.smi')
    
    
# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('HER2.pkl', 'rb'))
    # Apply model to make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[0], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)



# Page title
st.markdown("""
# HER2 Inhibition Predictor """)

st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>""", unsafe_allow_html = True)

st.markdown('<p class="big-font"> This app allows users to predict how strongly a molecule will inhibit HER2 (human epidermal growth factor receptor 2).</p>', unsafe_allow_html = True)

st.markdown('<p class = "big-font"> HER2 is a protein that is overexpressed in around 25% of breast cancers. Therapies that specifically inhibit HER2 such as traztuzumab have recently proven to be effective, but newer and improved therapies with fewer side effects are still needed. </p>', unsafe_allow_html = True)

st.markdown("""<p class = "big-font">This application will predict pIC50, a measure of how potently a molecule inhibits HER2 activity. Molecules with pIC50 values of 7+ are considered potent inhibitors. The model was trained using a large dataset of IC50 values obtained from <a href = "https://www.ebi.ac.uk/chembl/" >ChEMBL</a>, and molecular descriptors generated using the <a href = "https://onlinelibrary.wiley.com/doi/10.1002/jcc.21707">PaDEL software</a>. After testing multiple models, a hyperparameter-optimized Random Forest Regressor was used (R² value of 0.71 and MSE of 0.34).</p>""", unsafe_allow_html = True)

st.markdown("""<p class = "big-font"><strong>Credits</strong></p>""", unsafe_allow_html = True)




st.markdown('<ul><li class = "big-font"> Streamlit template & resources from <a href = "https://data-professor.medium.com/">Dr. Chanin Nantasenamat</a></li><li class = "big-font"><a href = "https://github.com/PascalSpiegler/her2-inhibition">Source Code</a></li>', unsafe_allow_html = True)
                    


# Sidebar
with st.sidebar.header('1. Upload your input file'):
    st.sidebar.markdown('[Example input file](https://raw.githubusercontent.com/PascalSpiegler/bioactivities/main/HER2_example_input.txt)')
    agree = False
    agree = st.sidebar.checkbox("""Use example input""")
    if agree:
        uploaded_file = 'https://raw.githubusercontent.com/PascalSpiegler/bioactivities/main/HER2_example_input.txt'
    else:
        uploaded_file = st.sidebar.file_uploader("Include SMILES ID followed by CHEMBL ID for each molecule (separated by space as a .txt file)", type=['txt'])


if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating descriptors..."):
        desc_calc(load_data)

    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.write(desc.shape)

    # Read descriptor list used in previously built model
    st.header('**Removing features irrelevant to our model**')
    Xlist = list(pd.read_csv('descriptor_list.csv').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)

    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    if not agree:
        st.info('Upload input data in the sidebar to start!')
