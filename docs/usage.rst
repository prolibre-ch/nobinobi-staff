=====
Usage
=====

To use Nobinobi Staff in a project, add it to your `INSTALLED_APPS`:

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
        url(r'^', include(nobinobi_staff_urls)),
        ...
    ]
