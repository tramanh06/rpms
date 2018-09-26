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


Download papers collection and dataset from AISG's team drive and extract
under the project root folder.

`AI Technology / TramAnh Handover`

https://drive.google.com/open?id=10Qo7JuXZ4mv6YPKtDBSBuklUHKp9c1O8




## Project Structure

These are the important folders and files that should help you get started

| Files | Explanation |
|-------|-------------|
| `main_download_papers.py` | Purpose of this file is to download papers belonged to researchers given a list of researchers (txt file, line-delimited). This file mainly used methods from `paper_crawling/` folder. Downloaded papers are stored under `papers/` |
| `main_build_corpus.py` | Process pdf papers and parse to text. Stemming and remove of stopwords and strange characters as well. |
| `main_match_paper.py` | Build corpus and word vector. Cosine similarity is used to match paper | 
| `notebooks/Author-Topic_Model_2.ipynb` | Topic modelling of researchers papers based on Author-Topic LDA Model |

Everytime a .py file is run, a log file will also be created and stored under `logs/`
with timestamp, file details and log warning level, so that it's easy to monitor. 


## To run 
### Download Papers
To download papers from a list of researchers

```
python main_download_papers.py --researchers researchers.txt
```

The process will crawl dblp for list of papers and store the (researcher, papers) information 
in a pickled file, `researchers_to_papers.p`. 

`main_download_papers.py` will first crawl from arxiv, if not found, it'll query 
Google using Google Search API. Currently, Google API is used under Tram Anh's credentials
and stored under `venv/keys.ini` (**do not** check in this file into version control, especially Github).
We can only query 100 queries/day under free version. Therefore, a pickled file is used to keep
track of what's left to query for the next day. The counter reset at 3pm Singapore time every day.

To download papers from pickled file

```
python main_download_papers.py --pickled researchers_to_papers.p
```

### Build Corpus

To run
```
python main_build_corpus.py
```

This process will do the following:

1. Parse pdf papers to text
2. Preprocess text (stem, remove stopwords, remove non-English words and strange characters)

Output is written under `bow/`, 1 pdf = 1 `*.bow` file. There is one master output under *each* author folder, called `_.json`. For example, `bow/Bryan_Low/_.json`. There is also one master output of *ALL* the researchers, produced and saved as `papers.json` in the main directory.

Most preprocessing parameters are stored in `config.ini`. See comments in that file
for more details to tune. 


### Match Papers

To run 
```
python main_match_paper.py -d <Link_to_pdf_location>
```

This class is straight-forward. The program will parse the pdf, preprocess build
a Bag-Of-Word for it. Tf-idf is created and is compared with existing researchers'
tfidf using cosine similarity to find a ranking of relevant researchers. 


### Topic-Model 

All the code for this is in a notebook under `notebooks/Author-Topic_Model_2.ipynb`.
The code is based on the Author-Topic Model from [1]. Intermediate representation 
of the link between papers and authors are stored under `dataset/`.

This needs to do more tuning as more authors and papers are downloaded. There are 
20 topics set for LDA right now. For each topic, there is a user-defined topic name
for easy reference. However, when more papers and authors are present, the
topic distribution will change and the topic names would need to be changed accordindly.



References
----------

http://papermatching.cs.toronto.edu/

[1] The Author-Topic Model for Authors and Documents