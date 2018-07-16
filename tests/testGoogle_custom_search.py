import urllib


def test_download_url_without_pdf():
    pdf_url = "https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=4039&context=sis_research"
    # pdf_url "http://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=3995&context=sis_research"
    outfile = "Scalable_transfer_learning_in_heterogeneous_dynamic_environments.pdf"

    urllib.urlretrieve(pdf_url, outfile)


def test_download_nonpdf_link():
    # pdf_url = "https://www.computer.org/csdl/proceedings/icpr/2014/5209/00/5209d245.pdf"
    pdf_url = "http://www.ifaamas.org/Proceedings/aamas2016/pdfs/p1411.pdf"
    outfile = "Automated_Prediction_of_Glasgow_Outcome_Scale_for_Traumatic_Brain_Injury.pdf"
    result = urllib.urlretrieve(pdf_url, outfile)
    print result[1]['content-type'] == 'application/pdf'

test_download_nonpdf_link()