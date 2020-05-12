Improved GeoJSON datasets for data.stad.gent  
============================================

[![license-badge]](LICENSE)


The [Open Data portal of the City of Ghent](https://data.stad.gent/datasets) has a collection of
datasets can can be downloaded in different formats, like XML, KML, JSON or GeoJSON. The **problem with
the GeoJSON responses** is that they normally only contain `MultiPolygon` or `MultiPoint` collections
of coordinates and very little extra information (it seems the City of Ghent is not using the latest version
of [The DataTank](http://thedatatank.com/), that fixes this).

This simple application reads the associated KML files to **generate more complete GeoJSON** responses.

How to use it
-------------

You can access the data at [https://geogent.herokuapp.com/](https://geogent.herokuapp.com/).
To make a request you just need to replace the City of Ghent DataTank domain `datatank.stad.gent` with
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

The application uses [Pipenv](https://docs.pipenv.org/) to manage Python packages:

    $ pipenv install --dev
    $ pipenv shell

Update dependencies (and manually update `requirements.txt`):

    $ pipenv update --dev && pipenv lock -r

Running the server
------------------

    $ python runserver.py

Style guide
-----------

    $ black geogent


Heroku
======

Use Heroku Containers to deploy the app:

    $ heroku login
    $ heroku stack:set container
    $ git push heroku master


[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg
