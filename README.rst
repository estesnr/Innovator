==========
aras-tools
==========

Methods to encapsulate API calls to the ARAS Innovator database
like uploading files or viewing information on parts and documents.

Description
===========

Example Usage:

Here is an example code needed to create an API object to use the methods.

.. code-block:: python
    from parts import PartsAPI

    parts_api = PartsAPI(
        base_url="https://innovator.hangar18.io/InnovatorServer",
        database="InnovatorSample",
        client_id="TestApp",
        username="admin"
    )

    # after prompting you for a password, the object to access the methods
    # will be available

    # here we will create some data for a part to create in our database.
    # make a note of the valid keys in the method for authorized data types
    # that can be used.
    metadata = {
        "item_number": "Example Part",
        "description": "EyeBolt"
    }

    # then we use the data to create our part.
    parts_api.create_part(metadata)

    # we can verify the part was made and view the data with another method
    parts_api.search_part_type("EyeBolt")

    # this should give us a json readout consisting of all parts in the
    # database that are listed as EyeBolts.
