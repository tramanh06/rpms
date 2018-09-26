RPMS - Reviewer-Paper Matching System
-------------------------------------

A text-based system to match 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine 
for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
It is recommended to use virtualenv for a clean dependency managament. The code below will
install dependencies for the project, once a virtual environment has been activated.

```
virtualenv -p python2.7 venv
source venv/bin/activate
pip install -r requirements.txt
```

Install unix package pdftotext - needed to convert pdf to txt file
```brew cask install pdftotext```


Install Spacy's English dictionary - needed for tokenization
```python -m spacy download en```


## Project Structure

These are the important folders and files that should help you get started

Files | Explanation |
`main_download_papers.py` | Purpose of this file is to download papers belonged to researchers 
given a list of researchers (txt file, line-delimited). This file mainly used methods from 
`paper_crawling/` folder. Downloaded papers are stored under `papers/` |
`main_build_corpus.py` | Process pdf papers and parse to text. Stemming and remove of stopwords
and strange characters as well. Output is written under `bow/`, 1 pdf = 1 `*.bow` file. There is one 
master output under *each* author folder, called `_.json`. For e.g., `bow/Bryan_Low/_.json`.
There is also one master output of *ALL* the researchers, produced and saved as `papers.json` 
in the main directory |
`main_match_paper.py` | Build corpus and word vector. Cosine similarity is used to match paper | 
`notebooks/Author-Topic_Model_2.ipynb` | Topic modelling of researchers papers 
based on Author-Topic LDA Model
`researchers.txt` 

References
----------

https://bitbucket.org/lcharlin/tpms

http://papermatching.cs.toronto.edu/
