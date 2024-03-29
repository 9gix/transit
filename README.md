# Transit Django Project #
## Prerequisites ##

- python >= 2.7
- pip
- virtualenv/wrapper (optional)

## Installation ##
### Creating the environment ###
Create a virtual python environment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```bash
mkvirtualenv --no-site-packages transit-env
```

#### For virtualenv ####
```bash
virtualenv --no-site-packages transit-env
cd transit-env
source bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone <URL_TO_GIT_RESPOSITORY> transit
```

### Install requirements ###
```bash
cd transit
pip install -r requirements.txt
```

### Configure project ###
```bash
cp transit/__local_settings.py transit/local_settings.py
vi transit/local_settings.py
```

### Sync database ###
```bash
python manage.py syncdb
python manage.py migrate
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000
