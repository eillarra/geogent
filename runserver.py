import os

from flask import Flask, jsonify
from flask_cache import Cache
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


app = Flask(__name__)
cache = Cache(app, config=CACHE_CONFIG)


def parse_coordinates(string):
    points = []
    for point in string.split(' '):
        if point:
            points.append([float(x) for x in point.split(',')[:2]])
    return Point(points[0]) if len(points) == 1 else Polygon([points])


@app.route('/<int:v>/<string:category>/<string:dataset>.geojson')
@cache.cached(timeout=5 * 60 * 60)
def get_dataset(v, category, dataset):
    datatank = 'https://datatank.stad.gent/'
    key = str(v) + '/' + category + '/' + dataset

    try:
        source = get(datatank + key + '.kml').text.encode('utf-8')
        tree = etree.fromstring(source, parser=etree.XMLParser(ns_clean=True))
    except:
        return jsonify({
            'error': 'Sorry, but we could not find the requested dataset'
        }), 404

    nsm = tree.nsmap
    nsm['kml'] = nsm.pop(None)
    features = []

    for element in tree.xpath('//kml:Placemark', namespaces=nsm):
        properties = {}

        for d in element.xpath('.//kml:SimpleData', namespaces=nsm):
            value = d.text
            try:
                properties[d.attrib['name'].lower()] = int(value) if value.isdigit() else value
            except:
                properties[d.attrib['name'].lower()] = None

        if 'naam' in properties:
            properties['title'] = properties['naam']

        geometry = parse_coordinates(element.find('.//kml:coordinates', namespaces=nsm).text)
        features.append(Feature(geometry=geometry, properties=properties))

    return jsonify(FeatureCollection(features, properties={
        'title': tree.xpath('//kml:Document/kml:Folder/kml:name', namespaces=nsm)[0].text,
        'source': datatank + key + '.geojson',
    }))


if __name__ == '__main__':
    app.run(debug=DEBUG)
