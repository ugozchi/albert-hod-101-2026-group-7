# Assignment 1: TF-IDF Matrix

## Description
This assignment implements a TF-IDF matrix builder from scratch without using Scikit-learn.

## Structure
- `scripte/`: Contains the Python script for building the TF-IDF matrix
- `source/`: Contains the source data files (CSV)

## Features
The implementation includes:
- **Text preprocessing**:
  - Removal of punctuation and special characters (using regex)
  - Removal of numbers (using regex)
  - Removal of words with less than 3 letters
  - Tokenization of the data

- **TF-IDF calculation**:
  - Term Frequency (TF): `(number of times term appears in document) / (total number of terms in document)`
  - Inverse Document Frequency (IDF): `log(total number of documents / number of documents containing the term)`
  - TF-IDF: `TF × IDF`

## Usage
Run the script:
```bash
python scripte/tf_idf_matrix.py
```

## Note
Scikit-learn is **not authorized** for this assignment. All calculations are implemented manually.
