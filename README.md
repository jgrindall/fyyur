
## Development Setup

1. git clone 

2. Use Python 3.10 for the following:

3. Install dependencies:

```
pip install -r requirements.txt
```


4. Create a .env file in the project root (fyyur/.env)

5. Add your postgres password to the .env file in the following format:

```
POSTGRES_PWD=<this is my password>
```

6. Setup a database called fyyur

7. Create tables using:

```
./upgrade.sh
```

8. Run the dev server:

```
./run.sh
```







