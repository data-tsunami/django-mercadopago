
* Remove '-dev' from version

    vim setup.py
    VER="$(python setup.py --version)" && git commit -m 'Bump version: $VER' setup.py

* Upload to pypi TESTING

    python setup.py register -r https://testpypi.python.org/pypi
    python setup.py sdist upload -r https://testpypi.python.org/pypi
    TMPVE="/tmp/$(uuidgen)" && virtualenv $TMPVE && source $TMPVE/bin/activate
    pip install --pre -i https://testpypi.python.org/pypi django-mercadopago

* Create tag

    VER="$(python setup.py --version)" && git tag -a -m "Version ${VER}" "v${VER}"

* Upload to pypi

    python setup.py upload -r https://testpypi.python.org/pypi

* Bump version number, add '-dev'

    vim setup.py
    VER="$(python setup.py --version)" && git commit -m "Bump version: $VER" setup.py
