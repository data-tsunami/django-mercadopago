Run unittests
-------------

Create `sample_project/djmercadopago_sample_app_settings.py` and run:

    PYTHONPATH=. python sample_project/manage.py test djmercadopago


Remove '-dev' from version
--------------------------

    vim setup.py
    VER="$(python setup.py --version)" && git commit -m 'Bump version: $VER' setup.py


Upload to pypi TESTING
----------------------

    python setup.py register -r pypitest
    python setup.py sdist upload -r pypitest
    TMPVE="/tmp/$(uuidgen)" && virtualenv $TMPVE && source $TMPVE/bin/activate
    pip install --pre -i https://testpypi.python.org/pypi django-mercadopago


Create Git tag
--------------

    VER="$(python setup.py --version)" && git tag -a -m "Version ${VER}" "v${VER}"


Upload to pypi
--------------

    python setup.py register -r pypi
    python setup.py sdist upload -r pypi


Bump version number, add '-dev'
-------------------------------

    vim setup.py
    VER="$(python setup.py --version)" && git commit -m "Bump version: $VER" setup.py
