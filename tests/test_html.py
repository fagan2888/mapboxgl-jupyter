import os
import json
import base64

from mock import patch

import pytest

from mapboxgl.viz import *
from mapboxgl.errors import TokenError
from mapboxgl.utils import create_color_stops
from matplotlib.pyplot import imread


@pytest.fixture()
def data():
    with open('tests/points.geojson') as fh:
        return json.loads(fh.read())


@pytest.fixture()
def polygon_data():
    with open('tests/polygons.geojson') as fh:
        return json.loads(fh.read())


TOKEN = 'pk.abc123'


def test_secret_key_CircleViz(data):
    """Secret key raises a token error
    """
    secret = 'sk.abc123'
    with pytest.raises(TokenError):
        CircleViz(data, access_token=secret)


def test_secret_key_GraduatedCircleViz(data):
    """Secret key raises a token error
    """
    secret = 'sk.abc123'
    with pytest.raises(TokenError):
        GraduatedCircleViz(data, access_token=secret)


def test_secret_key_ChoroplethViz(polygon_data):
    """Secret key raises a token error
    """
    secret = 'sk.abc123'
    with pytest.raises(TokenError):
        ChoroplethViz(polygon_data, access_token=secret)


def test_token_env_CircleViz(monkeypatch, data):
    """Viz can get token from environment if not specified
    """
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', TOKEN)
    viz = CircleViz(data, color_property="Avg Medicare Payments")
    assert TOKEN in viz.create_html()


def test_token_env_GraduatedCircleViz(monkeypatch, data):
    """Viz can get token from environment if not specified
    """
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', TOKEN)
    viz = GraduatedCircleViz(data,
                             color_property="Avg Medicare Payments",
                             radius_property="Avg Covered Charges")
    assert TOKEN in viz.create_html()


def test_token_env_ChoroplethViz(monkeypatch, polygon_data):
    """Viz can get token from environment if not specified
    """
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', TOKEN)
    viz = ChoroplethViz(polygon_data, color_property="density")
    assert TOKEN in viz.create_html()


def test_html_color(data):
    viz = CircleViz(data,
                    color_property="Avg Medicare Payments",
                    access_token=TOKEN)
    assert "<html>" in viz.create_html()


def test_html_GraduatedCricleViz(data):
    viz = GraduatedCircleViz(data,
                             color_property="Avg Medicare Payments",
                             radius_property="Avg Covered Charges",
                             access_token=TOKEN)
    assert "<html>" in viz.create_html()


def test_html_ChoroplethViz(polygon_data):
    viz = ChoroplethViz(polygon_data,
                        color_property="density",
                        color_stops=[[0.0, "red"], [50.0, "gold"], [1000.0, "blue"]],
                        access_token=TOKEN)
    assert "<html>" in viz.create_html()


@patch('mapboxgl.viz.display')
def test_display_CircleViz(display, data):
    """Assert that show calls the mocked display function
    """
    viz = CircleViz(data,
                    color_property="Avg Medicare Payments",
                    label_property="Avg Medicare Payments",
                    access_token=TOKEN)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_GraduatedCircleViz(display, data):
    """Assert that show calls the mocked display function
    """
    viz = GraduatedCircleViz(data,
                             color_property="Avg Medicare Payments",
                             label_property="Avg Medicare Payments",
                             radius_property="Avg Covered Charges",
                             radius_function_type="match",
                             color_function_type="match",
                             radius_default=2,
                             color_default="red",
                             access_token=TOKEN)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_HeatmapViz(display, data):
    """Assert that show calls the mocked display function
    """
    viz = HeatmapViz(data,
                     weight_property="Avg Medicare Payments",
                     weight_stops=[[10, 0], [100, 1]],
                     color_stops=[[0, "red"], [0.5, "blue"], [1, "green"]],
                     radius_stops=[[0, 1], [12, 30]],
                     access_token=TOKEN)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_ClusteredCircleViz(display, data):
    """Assert that show calls the mocked display function
    """
    viz = ClusteredCircleViz(data,
                     radius_stops=[[10, 0], [100, 1]],
                     color_stops=[[0, "red"], [10, "blue"], [1, "green"]],
                     access_token=TOKEN)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_ChoroplethViz(display, polygon_data):
    """Assert that show calls the mocked display function
    """
    viz = ChoroplethViz(polygon_data,
                        color_property="density",
                        color_stops=[[0.0, "red"], [50.0, "gold"], [1000.0, "blue"]],
                        access_token=TOKEN)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_vector_ChoroplethViz(display):
    """Assert that show calls the mocked display function when using data-join technique
    for ChoroplethViz.
    """
    data = [{"id": "06", "name": "California", "density": 241.7}, 
            {"id": "11", "name": "District of Columbia", "density": 10065}, 
            {"id": "25", "name": "Massachusetts", "density": 840.2}, 
            {"id": "30", "name": "Montana", "density": 6.858}, 
            {"id": "36", "name": "New York", "density": 412.3}, 
            {"id": "49", "name": "Utah", "density": 34.3}, 
            {"id": "72", "name": "Puerto Rico", "density": 1082}]

    viz = ChoroplethViz(data, 
                        vector_url='mapbox://mapbox.us_census_states_2015',
                        vector_layer_name='states',
                        vector_join_property='STATEFP',
                        data_join_property='id',
                        color_property='density',
                        color_stops=create_color_stops([0, 50, 100, 500, 1500], colors='YlOrRd'),
                        access_token=TOKEN
                       )
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_min_zoom(display, data):
    viz = GraduatedCircleViz(data,
                             color_property="Avg Medicare Payments",
                             label_property="Avg Medicare Payments",
                             radius_property="Avg Covered Charges",
                             access_token=TOKEN,
                             min_zoom=10)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_max_zoom(display, data):
    viz = HeatmapViz(data,
                     weight_property="Avg Medicare Payments",
                     weight_stops=[[10, 0], [100, 1]],
                     color_stops=[[0, "red"], [0.5, "blue"], [1, "green"]],
                     radius_stops=[[0, 1], [12, 30]],
                     access_token=TOKEN,
                     max_zoom=5)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_ImageVizPath(display, data):
    """Assert that show calls the mocked display function
    """

    image_path = os.path.join(os.path.dirname(__file__), 'mosaic.png')
    coordinates = [
        [-123.40515640309, 32.08296982365502],
        [-115.92938988349292, 32.08296982365502],
        [-115.92938988349292, 38.534294809274336],
        [-123.40515640309, 38.534294809274336]][::-1]

    viz = ImageViz(image_path, coordinates, access_token=TOKEN)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_ImageVizArray(display, data):
    """Assert that show calls the mocked display function
    """

    image_path = os.path.join(os.path.dirname(__file__), 'mosaic.png')
    image = imread(image_path)

    coordinates = [
        [-123.40515640309, 32.08296982365502],
        [-115.92938988349292, 32.08296982365502],
        [-115.92938988349292, 38.534294809274336],
        [-123.40515640309, 38.534294809274336]][::-1]

    viz = ImageViz(image, coordinates, access_token=TOKEN)
    viz.show()
    display.assert_called_once()


@patch('mapboxgl.viz.display')
def test_display_RasterTileViz(display, data):
    """Assert that show calls the mocked display function
    """
    tiles_url = 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'
    viz = RasterTilesViz(tiles_url, access_token=TOKEN)
