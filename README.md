Improved GeoJSON datasets for Ghent  
===================================

[![license-badge]](LICENSE)

The [Open Data portal of the City of Ghent](https://data.stad.gent/datasets) has a collection of
datasets can can be downloaded in different formats, like XML, KML, JSON or GeoJSON. The **problem with
the GeoJSON responses** is that they normally only contain `MultiPolygon` or `MultiPoint` collections
of coordinates and very little extra information.

This simple application reads the associated KML files to **generate more complete GeoJSON** responses.

How to use it
-------------
You can access the data at [https://geogent.herokuapp.com/](https://geogent.herokuapp.com/).
To make a request you just need to replace the City of Ghent Datatank domain `datatank.stad.gent` with
`geogent.herokuapp.com`. For example, the following URLs:

    https://datatank.stad.gent/4/cultuursportvrijetijd/speelterreinen.geojson
    https://datatank.stad.gent/4/mobiliteit/parkinglocaties.geojson

become:

    https://geogent.herokuapp.com/4/cultuursportvrijetijd/speelterreinen.geojson
    https://geogent.herokuapp.com/4/mobiliteit/parkinglocaties.geojson


For developers
==============

`geogent` uses [Flask](http://flask.pocoo.org/). Feel free to contribute to the project.

Application dependencies
------------------------
The application uses the [pip Package Manager](http://pip.readthedocs.org/en/latest/) to install dependencies.
While in development, you will need to read the dependencies from the following file:

    $ pip install -r requirements/development.txt

Running the server
------------------
    $ python runserver.py

Style guide
-----------
Tab size is 4 **spaces**. Maximum line length is 119. Furthermore your code has to validate against pyflakes.
It is recommended to use [flake8](https://pypi.python.org/pypi/flake8) which combines all the checks.


[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
