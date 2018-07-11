import os
import glob
import utils
import json
from pdf2bow import bow_phrases
import pickle

def extract_text_files(directory):
    all_txt = [utils.read_file(filename) for filename in glob.glob(directory + '*.txt')]
    return all_txt


def write_bow_text_to_individual_folder(researchers_to_bow, base_folder):
    for x in researchers_to_bow:
        output_file_location = os.path.join(base_folder, x['researcher'], "_with_phrases.all")
        utils.write_to_file(output_file_location, x['bow_content'])


def split_list_by_indices(list_, indices):
    return [list_[sum(indices[:i]) : sum(indices[:i+1])] for i in range(len(indices))]


if __name__ == '__main__':
    data_directory = "bow/"

    researchers_to_bow = []
    # Aggregate all text papers from sub-folder
    for o in os.listdir(data_directory):
        bow_sub_dir = os.path.join(data_directory, o, "")
        print "subdir = " + bow_sub_dir
        if os.path.isdir(bow_sub_dir):
            aggregated_texts = extract_text_files(bow_sub_dir)
            researchers_to_bow.append({'researcher': o, 'bow_content': aggregated_texts})

    # Store number of author's publications in a list, e.g. [10, 8, 11, ..]. Needed for later
    num_publications = [len(x['bow_content']) for x in researchers_to_bow]
    print "List of number of publications: "
    print num_publications
    
    stream_of_docs = [paper for x in researchers_to_bow for paper in x["bow_content"]]  # Flatten a list of list
    tokenized_docs, bigram_model = bow_phrases.text_preprocess_with_phrases(stream_of_docs)
    pickle.dump(bigram_model, open("bigram_model.p", "wb"))

    unflattened_docs = split_list_by_indices(tokenized_docs, num_publications)

    authors = [x['researcher'] for x in researchers_to_bow]

    researchers_to_bow_with_phrases = []
    for author, text_tokens in zip(authors, unflattened_docs):
        aggregated_texts = ' '.join([word for paper in text_tokens for word in paper])
        researchers_to_bow_with_phrases.append({'researcher': author, 'bow_content': aggregated_texts})
        utils.write_to_file(os.path.join(data_directory, author, "_with_phrases.all"), aggregated_texts)
    
    with open("data_with_phrases.json", 'wb') as f:
        json.dump(researchers_to_bow_with_phrases, f)



