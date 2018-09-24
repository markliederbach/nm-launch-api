===============================
nm_launch_api
===============================


API backend to search launch data to the frontend.


To Run Locally
--------------

1. Create a virtualenv

2. In the postactivate (or activate script), export the following environment variables:

.. code-block:: bash

    export NM_LAUNCH_API_SETTINGS=nm_launch_api.config.local
    export LAUNCH_LIBRARY_BASE_URL=https://launchlibrary.net/1.3

3. After you activate your virtualenv, from the root directory of the project, run:

.. code-block:: bash

    pip install -U .

4. Once the package is installed, simply run:

.. code-block:: bash

    <path to virtualenv>/bin/nm_launch_api

The API is now running on localhost port 8000.
