import streamlit as st
from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9202")


def search_es(query, index_name):
    """Perform a search query in Elasticsearch"""
    response = es.search(
        index=index_name,
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["absatz", "buch", "kapitel", "abschnitt_t"],
                    "fuzziness": "AUTO",
                }
            },
            "suggest": {
                "text-suggestions": {"text": query, "term": {"field": "absatz"}}
            },
        },
    )
    return response


# Streamlit UI
st.title("Gesetze Suche")
index_name = "gesetz"

with st.form(key="search_form"):
    query = st.text_input("Schreib Ihre Suchwahl:")
    submit_button = st.form_submit_button(label="Suchen")

if submit_button:
    if query:
        results = search_es(query, index_name)
        hits = results.get("hits", {}).get("hits", [])
        suggestions = (
            results.get("suggest", {})
            .get("text-suggestions", [{}])[0]
            .get("options", [])
        )

        if hits:
            if suggestions:
                st.subheader("Meinten Sie:")
                for suggest in suggestions:
                    st.write(suggest["text"])

            st.subheader("Resultate:")
            for hit in hits:
                st.write(hit["_source"]["buch"])
                st.write(
                    f"{hit['_source']['kapitel']}: {hit['_source']['abschnitt_n']} {hit['_source']['abschnitt_t']}"
                )
                st.write(hit["_source"]["absatz"])
                st.write("-----")

    else:
        st.write("Bitte geben Sie eine Suchanfrage ein.")
