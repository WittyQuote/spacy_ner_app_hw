# Running the Spacy Fun app

Install the requirements from requirements.txt using pip, and ensure that the spacy model "en_core_web_sm" has been downloaded (you can run ```python -m spacy download en_core_web_sm```
# Run the app

Open the terminal and run the spacy_fun_app.py file.

# Use the app once it's running

Interface to the spaCy entity extractor

## In the terminal
    
```
% curl -X POST -d@input.txt http://127.0.0.1:5000/api
{
  "input": "God is Japanese", 
  "output": "<markup>God is <entity class=\"NORP\">Japanese</entity></markup>"
}

% curl http://127.0.0.1:5000/api/entities 
[
  ("Japanese", "NORP")
]

```


## In a web browser

Go to [the site's address](http://0.0.0.1:5000/) and enter the text you are interested in running spaCy's NER model on, and submit the text. Then you should see the results on the page you are redirected to. On both pages there is a link to the entities page, which shows a table of all the entities the app has seen while this instance has been running.

## Building a docker image

Use Docker to build from the provided Dockerfile and then run the container image. For example:
```
% docker build -t spacy_fun:latest .
```
and then
```
docker run -d -p 80:80 spacy_fun:latest
```
then you can proceed as if it is running normally!
