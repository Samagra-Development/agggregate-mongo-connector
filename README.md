# Aggregate Mongo Connector
--------------------------------

This is a Flask server which provides endpoints to save and fetch data from odk to mongoDb respectively.

## Steps to Run

1 Go to src folder and make a create a new file ```.env```  and add your environment variables there. 
> You can find a sample .env file in src folder ```.env.sample```
```bash
		cp .env.sample .env
```

2 Create a new virtual environment(Refer [here](https://docs.python.org/3/library/venv.html)) or in your existing python environment install the requirements.txt
```bash
		pip install -r requirements.txt
```
3 After all the dependencies are installed, run the Flask server
```bash
		python app.py
```