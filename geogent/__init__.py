import json
import os

from flask import Flask, Response, send_from_directory
from flask_caching import Cache
from geojson import FeatureCollection, Feature, Point, Polygon
from lxml import etree
from requests import get


if 'REDIS_URL' in os.environ:
    DEBUG = False
    CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.environ.get('REDIS_URL'),
    }
else:
    DEBUG = True
    CACHE_CONFIG = {'CACHE_TYPE': 'null'}

DATATANK = 'https://datatank.stad.gent/4/'


app = Flask(__name__)
cache = Cache(app, config=CACHE_CONFIG)


def parse_coordinates(string):
    points = []
    for point in string.split(' '):
        if point:
            points.append([float(x) for x in point.split(',')[:2]])
    return Point(points[0]) if len(points) == 1 else Polygon([points])


@app.errorhandler(404)
def page_not_found(e):
    res = json.dumps({
        'error': 'Sorry, but we could not find the requested page'
    })

    return Response(response=res, status=404, mimetype='application/json')


@app.route('/4/<string:category>/<string:dataset>.geojson')
@cache.cached(timeout=24 * 60 * 60)
def get_dataset(category, dataset):
    key = category + '/' + dataset

    try:
        source = get(DATATANK + key + '.kml').text.encode('utf-8')
        tree = etree.fromstring(source, parser=etree.XMLParser(ns_clean=True))
    except Exception as e:
        return page_not_found(e)

    nsm = tree.nsmap
    nsm['kml'] = nsm.pop(None)
    features = []

    for el in tree.xpath('//kml:Placemark', namespaces=nsm):
        properties = {}

        for prop in el.xpath('.//kml:SimpleData', namespaces=nsm):
            value = prop.text
            try:
                properties[prop.attrib['name'].lower()] = int(value) if value.isdigit() else value
            except Exception as e:
                properties[prop.attrib['name'].lower()] = None

        if 'naam' in properties:
            properties['title'] = properties['naam']

        geometry = parse_coordinates(el.find('.//kml:coordinates', namespaces=nsm).text)
        features.append(Feature(geometry=geometry, properties=properties))

    res = json.dumps(FeatureCollection(features, properties={
        'title': tree.xpath('//kml:Document/kml:Folder/kml:name', namespaces=nsm)[0].text,
        'source': DATATANK + key,
    }))

    return Response(response=res, status=200, mimetype='application/vnd.geo+json')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/4/')
@app.route('/')
@cache.cached(timeout=30 * 24 * 60 * 60)
def index():
    res = json.dumps({
        'info': 'Check the Open Data portal of the City of Ghent for available datasets; then, simply replace '
                '`datatank.stad.gent` for `geogent.herokuapp.com` when requesting GeoJSON datasets.',
        'url': DATATANK
    })

    return Response(response=res, status=200, mimetype='application/json')
