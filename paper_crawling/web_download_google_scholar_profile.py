#!/usr/bin/python -u

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import glob
import os
import re
import download_google_scholar_profile

REVIEWER_PAPER_LOC='/tmp/'
REVIEWER_GSCHOLAR_FILES='/tmp/gscholar/'

print "Content-type: text/html"
print

download=False
validate=False
form = cgi.FieldStorage()
if form.getvalue("validate_scholar_urls") is not None: 
    print 'asked to validate <p />'
    validate=True
elif form.getvalue("download_scholar_urls") is not None: 
    download=True
print """ 
<html>

<head><title>Google scholar harvester</title></head>

<body>
<form method="post" action="parse.py">
Enter reviewer information in the text box below.<br />
Format is: <br />
One reviewer per line<br />
ReviewerEmail,reviewer Gscholar URL[,number of papers to retrieve]<br />
e.g.: foo@bar.edu,http://scholar.google.com/citations?user=foo,5<br />
(last field is optional)<br />
<textarea cols="100" rows="15" name="scholar_urls_emails" wrap="off" >""" 

if validate or download: 
    print form.getvalue("scholar_urls_emails").strip(),

print """</textarea><br />
<input type="submit" name="validate_scholar_urls" value="Validate input">
<input type="submit" name="download_scholar_urls" value="Download reviewer papers">
</form>

</body>
"""

#form = cgi.FieldStorage()
#if form.getvalue("validate_scholar_urls"): 
#    print 'asked to validate'
#    validate=True
if form.getvalue("download_scholar_urls"): 
    print 'asked to download<p />'
    download=True

download_google_scholar_profile.createDir(REVIEWER_GSCHOLAR_FILES)

scholar_urls_emails = form.getvalue("scholar_urls_emails")
if scholar_urls_emails is not None: 

    print "Found ", len(scholar_urls_emails.split('\n')), "reviewers <p />" 
    for url_email in scholar_urls_emails.split('\n'): 
        if len(url_email.strip()) != 0: 
            url_email_splitted = url_email.split(',')
            if len(url_email_splitted) == 3:
                reviewer_email, gScholar_reviewer_url, num_papers_to_retrieve = url_email_splitted
            elif len(url_email_splitted) == 2:
                reviewer_email, gScholar_reviewer_url = url_email_splitted
                num_papers_to_retrieve = None
            else: 
                print 'Invalid input: ', url_email
                continue 

            if validate:
                print 'reviewer Email, reviewer Scholar URL<br />'
            print reviewer_email, ',', gScholar_reviewer_url, ',', 
            if num_papers_to_retrieve is not None: 
                num_papers_to_retrieve = int(num_papers_to_retrieve)
                print num_papers_to_retrieve,
            print '<br />'

            if download:
                # get reviewer's profiles files
                reviewerDir=REVIEWER_PAPER_LOC+reviewer_email+'/'
                reviewerTmpDir=REVIEWER_GSCHOLAR_FILES+reviewer_email+'/'
                reviewerFiles = []
                if os.path.exists(REVIEWER_PAPER_LOC+reviewer_email): 
                    print 'reviewer already has files in the system<br />'
                    # There are a couple of cases here: 
                    # 1- Reviewer is unknown to the system -> d/l data from gscholar
                    # 2- Reviewer is known to the system but we've already downloaded data from gscholar -> d/l data from gscholar
                    # 3- Reviewer is known -> do not d/l from gscholar
                    # known to the system here implies a file in REVIEWER_PAPER_LOC+reviewer_email
                    # One potential problem is for future use of this script, will we be able to figure out what papers are from gscholar... 
                    # UPDATE: yes we will
                    # TODO: add a condition that says that if the profile was
                    # changed (file deleted or file uploaded) manually more recently than the google
                    # profile download then we do not allow the download. 
                    if not os.path.exists(reviewerTmpDir) and len(glob.glob(reviewerDir+'*'))>0:
                        print 'To prevent clobbering, not allowing further download of reviewer data<br />' 
                        continue
                    else:
                        print 'Reviewer profile is either empty or it already was populated with google scholar profile.' 

                    for f in glob.glob(reviewerDir+'*'):
                        reviewerFiles += [download_google_scholar_profile.fileHash(f)]
                else:
                    print 'reviewer unknown'

                # Start download process
                print '<h5><pre>'
                
                if num_papers_to_retrieve is not None: 
                    download_google_scholar_profile.getReviewer(gScholar_reviewer_url,reviewer_email,reviewerDir,reviewerFiles,reviewerTmpDir=reviewerTmpDir,numPapersToRetrieve=num_papers_to_retrieve)
                else:
                    download_google_scholar_profile.getReviewer(gScholar_reviewer_url,reviewer_email,reviewerDir,reviewerFiles,reviewerTmpDir=reviewerTmpDir)
                print '</pre></h5>'

print """</html>""" 
