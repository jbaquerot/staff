==========
WorkOrders
==========

WorkOrders is a simple Django app to manage the work orders for external staff and calculate the invoice distribution between the projects

TODO: Detail documentation is in the "docs" directory

Quick start
-----------

1. Add "workOrders" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'workOrders',
    )

3. Run `python manage.py migrate` to create the workOrders models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a workOrder (you'll need the Admin app enabled).
