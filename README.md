# HER2 Inhibition Predictor

This app uses a hyperparameter-optimized Random Forest Regressor to predict how strongly a molecule will inhibit HER2 (human epidermal growth factor receptor 2). The model was trained using a large dataset of IC50 values obtained from [ChEMBL](https://www.ebi.ac.uk/chembl/), and molecular descriptors generated using the [PaDEL software](https://onlinelibrary.wiley.com/doi/10.1002/jcc.21707).

## Preview
[https://her2-inhibition.streamlit.app](https://her2-inhibition.streamlit.app/)

## Local setup instructions:

### Create a conda environment
```
conda create -n inhibition

conda activate inhibition
```
### Install the prerequisite libraries
```
pip install -r requirements.txt
```

###  Launch the app
```
streamlit run "HER2.py"
```

##  Credits
Thank you to [Dr. Chanin Nantasenamat](https://data-professor.medium.com/) for his bioinformatics resources and Streamlit template.
