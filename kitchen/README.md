# kitchen

Simple cookbook for running the zeus project inside the virtualbox VM through with vagrant.

To use it you need virtualbox, vagrant and chefdk.

## How to use it

    kitchen create
    kitchen converge
    kitchen login

Then follow it up with instructions from zeus README:

    cd zeus
    pipenv shell

    cp settings/local_template.py settings/local.py

    python manage.py migrate

    python manage.py manage_users --create-institution "ZEUS"
    python manage.py manage_users --create-user <username> --institution=1

To test system:

    pytest -v

## How to run system locally

Add to your `settings/local.py` file:

    ALLOWED_HOSTS = ['*']

And run the server:

    python manage.py runserver 10.0.42.42:8000

## Windows notes

### Problem with pip crashing when trying to guess coding page of windows console

To [solve that issue](https://github.com/pypa/pip/issues/4251#issuecomment-279117184) - check your coding page:

    chcp

Example result could be `852`.

Then use your text editor to open pip file `lib/site-package/pip/compat/__init__.py` for your pipenv.
Around line 75, change

    return s.decode('utf_8')

to (for example)

    return s.decode('cp852')

### Missing gmpy2

To [install it separately](https://stackoverflow.com/a/40076291/1334531) - use file put in the `windows` dir:

    pipenv shell
    pip install kitchen\windows\gmpy2-2.0.8-cp36-cp36m-win_amd64.whl
    exit

### Missing uwsgi

Hoping that uswgi is required only for production.
We comment out(or remove) uwsgi line in `Pipfile` and continue.
