"""Make search index."""

import argparse
from collections import Counter, defaultdict
import csv
import json
from math import log
from pathlib import Path
import sys


# [main]
def main():
    """Main driver."""
    args = parse_args()
    abstracts = read_abstracts(args.bibdir)
    words_in_file = {
        filename: get_words(abstract) for filename, abstract in abstracts.items()
    }
    term_freq = calculate_tf(words_in_file)
    inverse_doc_freq = calculate_idf(words_in_file)
    tf_idf = calculate_tf_idf(term_freq, inverse_doc_freq)
    save(args.outfile, tf_idf)
# [/main]


# [calculate_idf]
def calculate_idf(words_in_file):
    """Calculate inverse document frequency of each word."""
    num_docs = len(words_in_file)
    word_sets = [set(words) for words in words_in_file.values()]
    result = {}
    for word in set().union(*word_sets):
        result[word] = log(num_docs / sum(word in per_doc for per_doc in word_sets))
    return result
# [/calculate_idf]


# [calculate_tf]
def calculate_tf(words_in_file):
    """Calculate term frequency of each word per document."""
    result = {}
    for filename, wordlist in words_in_file.items():
        total_words = len(wordlist)
        counts = Counter(wordlist)
        for w in wordlist:
            result[(filename, w)] = counts[w] / total_words
    return result
# [/calculate_tf]


# [calculate_tf_idf]
def calculate_tf_idf(term_freq, inverse_doc_freq):
    """Calculate overall score for each term in each document."""
    result = defaultdict(dict)
    for (filename, word), tf in term_freq.items():
        result[word][filename] = tf * inverse_doc_freq[word]
    return result
# [/calculate_tf_idf]


# [get_words]
def get_words(text):
    """Get words from text, stripping basic punctuation."""
    words = text.split()
    for char in ",.'\"()%‰!?$‘’&~–—±·":
        words = [w.strip(char) for w in words]
    return [w for w in words if w]
# [/get_words]


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bibdir", type=str, required=True, help="bibliography directory"
    )
    parser.add_argument("--outfile", type=str, default=None, help="output file")
    return parser.parse_args()


# [read_abstracts]
def read_abstracts(bibdir):
    """Extract abstracts from bibliography entries."""
    result = {}
    for filename in Path(bibdir).iterdir():
        data = json.loads(Path(filename).read_text())
        result[filename.name] = data["abstract"]
    return result
# [/read_abstracts]


# [save]
def save(outfile, tf_idf):
    """Save results as CSV."""
    outfile = sys.stdout if outfile is None else open(outfile, "w")
    writer = csv.writer(outfile)
    writer.writerow(("word", "doc", "score"))
    for word in sorted(tf_idf):
        for filename, score in sorted(tf_idf[word].items()):
            writer.writerow((word, filename, score))
    outfile.close()
# [/save]


if __name__ == "__main__":
    main()
