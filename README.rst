=============================
Nobinobi Staff
=============================

.. image:: https://badge.fury.io/py/nobinobi-staff.svg
    :target: https://badge.fury.io/py/nobinobi-staff

.. image:: https://travis-ci.org/prolibre-ch/nobinobi-staff.svg?branch=master
    :target: https://travis-ci.org/prolibre-ch/nobinobi-staff

.. image:: https://codecov.io/gh/prolibre-ch/nobinobi-staff/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/prolibre-ch/nobinobi-staff

.. image:: https://pyup.io/repos/github/prolibre-ch/nobinobi-staff/shield.svg
     :target: https://pyup.io/repos/github/prolibre-ch/nobinobi-staff/
     :alt: Updates

.. image:: https://pyup.io/repos/github/prolibre-ch/nobinobi-staff/python-3-shield.svg
     :target: https://pyup.io/repos/github/prolibre-ch/nobinobi-staff/
     :alt: Python 3

Application staff for nobinobi

Documentation
-------------

The full documentation is at https://nobinobi-staff.readthedocs.io.

Quickstart
----------

Install Nobinobi Staff::

    pip install nobinobi-staff

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'nobinobi_staff.apps.NobinobiStaffConfig',
        ...
    )

Add Nobinobi Staff's URL patterns:

.. code-block:: python

    from nobinobi_staff import urls as nobinobi_staff_urls


    urlpatterns = [
        ...
        path('', include(nobinobi_staff_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
