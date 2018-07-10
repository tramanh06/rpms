RPMS - Reviewer-Paper Matching System
----

The code is forked from Toronto Paper Matching System. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine 
for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
It is recommended to use virtualenv for a clean dependency managament. The code below will
install dependencies for the project, once a virtual environment has been activated.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Unix package pdftotext is needed to convert pdf to txt file
`brew cask install pdftotext`


Spacy's English dictionary is needed for tokenization later
`python -m spacy download en`


References
----------

https://bitbucket.org/lcharlin/tpms

http://papermatching.cs.toronto.edu/
