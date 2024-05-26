# gesetz_buche

This is an improved search interface of the online version [German law books](https://www.gesetze-im-internet.de/).
This service adds fuzzy text matching and suggested corrections.

The textual law is parsed via `parse_gesetz.py`, and indexed on an ElasticSearch DB (docker image).
The search interface itself is powered via a `streamlit` server.

To activate both, run

```bash
docker compose up -d
streamlit run app.py
```