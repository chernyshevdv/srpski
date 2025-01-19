# Setup

## Environment variables

The following environment variables need to be created:
* DJANGO_SECRET_KEY
* DJANGO_DEBUG

The following script might run with `ENV_FILE` set depending on the environment:

```sh
export ENV_FILE=.env
echo "export DJANGO_SECRET_KEY=$(openssl rand -base65 50) >> $ENV_FILE
echo "export DJANGO_DEBUG=true" >> $ENV_FILE
```

### In production environment

Ensure that you put the following strings in the WSGI config file:

```python
from dotenv import load_dotenv
load_dotenv(os.path.join(path, '.env'))
```
`path` variable should have been set to where the `.env` file resides 
(usually it's different from `wsgi.settigns` file location).

### In dev environment
You can set those variables in the OS enviroment
by just pointing ENV_FILE variable to `~/.zshrc` instead of `.env`.

Alternatively, you can create `.env` file also.
