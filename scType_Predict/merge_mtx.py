import scanpy.api as sc
import os
import glob
import re
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

pd.options.display.max_colwidth = 150

def merge_mtx(filepath):

    os.chdir(filepath)
    files = glob.glob("*.mtx")
    samples = [f.replace('.mtx', '') for f in files]
    sample = samples.pop(0)

    sample_file = sample+'.mtx'
    barcode_file = sample+'_barcodes.tsv'
    gene_file = sample+'_genes.tsv'

    print("Processing file: ", sample)

    adata = sc.read(sample_file, cache=True).T
    barcodes = pd.read_table(barcode_file, header=None)
    genes = pd.read_table(gene_file, header=None)

    barcodes.rename(columns={0:'barcode'}, inplace=True)
    barcodes.set_index('barcode', inplace=True)
    adata.obs = barcodes
    genes.rename(columns={0:'gene_symbol'}, inplace=True)
    genes.set_index('gene_symbol', inplace=True)
    adata.var = genes

    for i in range(len(samples)):
        print("Processing file: ", samples[i])
        sample_file = samples[i]+'.mtx'
        barcode_file = samples[i]+'_barcodes.tsv'
        gene_file = samples[i]+'_genes.tsv'
        adata_tmp = sc.read(sample_file, cache=True).T
        barcodes = pd.read_table(barcode_file, header=None)
        genes = pd.read_table(gene_file, header=None)

        barcodes.rename(columns={0:'barcode'}, inplace=True)
        barcodes.set_index('barcode', inplace=True)
        adata_tmp.obs = barcodes

        genes.rename(columns={0:'gene_symbol'}, inplace=True)
        genes.set_index('gene_symbol', inplace=True)
        adata_tmp.var = genes

        adata = adata.concatenate(adata_tmp, join = 'outer')

        adata.write('all_merged_dge.h5')

def get_labels(filepath):
    
    os.chdir(filepath)
    files = glob.glob("*.mtx")
    samples = [f.replace('.mtx', '') for f in files]
    sample = samples.pop(0)
    label_file = sample+'_labels.tsv'
    labels = pd.read_table(label_file, header=None)

    for i in range(len(samples)):
        label_file = samples[i]+'_labels.tsv'
        tmp = pd.read_table(label_file, header=None)
        labels = labels.append(tmp)

    print(labels.shape)
    pd.DataFrame.to_csv(labels, 'all_merged_labels.csv')


def predict():
    print("Model summary")
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "data", "model_d0.4_n50_d0.4_n25_outca.hdf5")
    model = load_model(DATA_PATH)
    print(model.summary())

    labels = pd.read_csv(os.path.join(this_dir, "data", "all_merged_labels.csv"), index_col=0)
    y=np.ravel(labels.values)
    encoder = LabelEncoder()
    encoder.fit(y)

    ## load the test data
    to_test_genes = pd.read_csv(os.path.join(this_dir, "data", "test.txt"), header = None)
    uni_genes = pd.read_csv(os.path.join(this_dir, "data", "genenames.csv"), index_col=0)
    X_test = pd.DataFrame(index=np.unique(to_test_genes[0].append(uni_genes['index'])))
    X_test.insert(0,'expr',0)
    X_test.iloc[X_test.index.isin(to_test_genes[0]),0] = 1
    X_test = X_test[X_test.index.isin(uni_genes['index'])]
    X_test = X_test.reindex(uni_genes['index'])


    pred = model.predict(X_test.T)
    inverted = [encoder.inverse_transform([np.argmax(p)])for p in pred] # numpy array
    predicted = pd.Series(inverted)
    print('Predicted cell-type: ' +
          re.sub("[]]$","",re.sub(".*[[]","",predicted.to_string())))
    ##pd.DataFrame(predicted).to_csv('/home/icb/subarna.palit/annotation_tool/05052019/prediction_on_TM_facs_Lung_genesets.csv')
