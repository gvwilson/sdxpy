import json
import sys

from bs4 import BeautifulSoup
from expander import Expander


def read_json(filename):
    with open(filename, "r") as reader:
        return json.load(reader)


def read_template(filename):
    with open(filename, "r") as reader:
        doc = BeautifulSoup(reader.read(), "html.parser")
        return doc.find("html")


def main():
    variables = read_json(sys.argv[1])
    doc = read_template(sys.argv[2])
    expander = Expander(doc, variables)
    expander.walk()
    print(expander.getResult())


if __name__ == "__main__":
    main()
