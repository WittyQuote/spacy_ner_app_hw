# Installing the Spacy Fun app

Install the requirements from requirements.txt using pip.

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
{
  "Japanese": 1
}

```


## In a web browser

Go to [the site's address](http://127.0.0.1:5000/) and enter the text you are interested in running spaCy's NER model on, and submit the text. Then you should see the results on the page you are redirected to. On both pages there is a link to the entities page, which shows a table of all the entities the app has seen while this instance has been running.

# Future development

It might be wise to jsonify the 'database' of entities that app has seen and save them to produce continuity between instances of the app. For now, that is not needed.


