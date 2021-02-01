# tokenizer

Alpheios Tokenizer Service


To run development server with Docker:

```
docker build -t tokenizer .
docker run -p 5000:5000 tokenizer:latest gunicorn --bind 0.0.0.0:5000 manage:app
```

Example requests:

OpenAPI Schema (describes operations, requests and responses): 

`curl -X GET "http://localhost:5000/"`

Tokenize TEI XML: 

`curl -H "Content-Type: application/xml" -X POST -d @tests/fixtures/tei/ovidmet.xml "http://localhost:5000/tokenize/tei?lang=lat"`

Tokenize Plain Text:

`curl -H "Content-Type: text/plain" -X POST --data-binary @tests/fixtures/text/lineseg.txt "http://localhost:5000/tokenize/text?lang=lat"`

