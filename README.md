# scType_Predict

Introduction
============
scType_Predict is an easy-to-use python package that can be used to annotate clusters using the marker genes obtained in the cell-type marker discovery analysis for scRNA-seq data (for example).

The scType_Predict method
=========================
scType_Predict is based on an artificial neural network that is trained on the entire Mouse Cell Atlas.

Installation
============
Installing scType_Predict from PyPi using::

    pip install -e scType_Predict

Usage
================
Import scType_Predict as::

    from scType_Predict.merge_mtx import predict
    predict()
