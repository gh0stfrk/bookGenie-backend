# Book Genie
Backend API for [book-genie](https://github.com/gh0stfrk/BookGenie) the AI book recommendation application.

## Setup 
- Create a virtual environment in python 3.10 >
```bash
python3 -m venv venv
```
- Install all dependencies 
```bash
source ./venv/bin/activate
pip install -r requirements.txt
```
- Execute the `main.py` file
```bash
python3 main.py
```



## API credentials
- There are two API credentials broadly, actually three
- One is OPEN AI's API key, the other two are google service accounts, one for firebase backend, and the other to write logs to sheets
- Create an .env file inside the `app` directory
- Add an openai's api key inside and add monogdb credentials
```
OPENAI_API_KEY=<Your_key>
MONGO_USER=<mongo_username>
MONGO_PASSWORD=<mongo_password>
```
- create 2 service accounts name them `creds.json` and `creds2.json` and drop them in `app` directory

- after this you are good to go.

