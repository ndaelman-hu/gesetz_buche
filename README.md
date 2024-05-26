# gesetz_buche

This is an improved search interface of the online version [German law books](https://www.gesetze-im-internet.de/).
This service adds fuzzy text matching and suggested corrections.

The textual law is parsed via `parse_gesetz.py`, and indexed on an ElasticSearch DB (docker image).
To popualte the DB:

```bash
docker compose up -d
python parse_gesetz.py 
```

The search interface itself is powered via a `streamlit` server.
To activate it:

```bash
streamlit run app.py
```