from bs4 import BeautifulSoup
from copy import deepcopy
from elasticsearch import Elasticsearch, helpers
import os

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9202")

def parse_html(html_content):
    soup = BeautifulSoup(html_content, "lxml-xml")
    jurs: list[dict[str, str]] = []
    
    jur = {}
    for div in soup.find_all("div"):
        if "class" in div.attrs:
            if div.attrs["class"] == "jnnorm":
                if (h1 := div.find("h1")):
                    jur["buch"] = h1.get_text(separator=" ").strip()
                if (h2 := div.find("h2")):
                    jur["kapitel"] = h2.get_text(separator=" - ").strip()
                if (h3 := div.find("h3")):
                    if (jnenbez := h3.find("span", class_="jnenbez")):
                        jur["abschnitt_n"] = jnenbez.text.strip()
                    if (jnentitel := h3.find("span", class_="jnentitel")):
                        jur["abschnitt_t"] = jnentitel.get_text(separator=" - ").strip()
            elif div.attrs["class"] == "jnhtml":
                for absatz in div.find_all("div", class_="jurAbsatz"):
                    jur["absatz"] = absatz.get_text(separator=" ").strip().replace("\n", " ").replace("§", " §")
                    jurs.append(deepcopy(jur))
    return jurs


def process_html_files(file_path: str, parser=parse_html):
    with open(file_path, "r", encoding="iso-8859-1") as file:
        html_content = file.read()
        div_texts = parser(html_content)
        return div_texts


def create_index(index_name):
    # Create an index with basic settings and mappings if it doesn't already exist
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, ignore=400)  # 400 causes to ignore "Index Already Exists" error

def index_documents(docs, index_name):
    actions = [
        {
            "_index": index_name,
            "_source": doc
        }
        for doc in docs
    ]
    helpers.bulk(es, actions)


if __name__ == "__main__":
    es_index = "gesetz"
    create_index(es_index)
    for file in os.listdir("/home/nathan/Downloads"):
        if file.endswith(".html"):
            docs = process_html_files(f"/home/nathan/Downloads/{file}")
            index_documents(docs, es_index)
