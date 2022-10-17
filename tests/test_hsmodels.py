import pytest
import json
import os

from hsmodels.schemas.aggregations import GeographicRasterMetadataIn, GeographicFeatureMetadataIn, \
MultidimensionalMetadataIn, ReferencedTimeSeriesMetadataIn, TimeSeriesMetadataIn


def _load_json(filename):
    with open(os.path.join("tests", "outputs", filename)) as f:
        expected_str = f.read()
        return json.loads(expected_str)

def test_netcdf_extraction():
    json_metadata = _load_json("netcdf.json")
    del json_metadata["files"]

    del json_metadata["abstract"]
    del json_metadata["contributor"]
    del json_metadata["creator"]
    del json_metadata["relation"]
    del json_metadata["rights"]
    model = MultidimensionalMetadataIn(**json_metadata)

    model_json = json.loads(model.json())
    del model_json["language"]
    del model_json["additional_metadata"]
    assert json_metadata == model_json

def test_rasters_extraction():
    json_metadata = _load_json("raster.json")
    del json_metadata["files"]

    model = GeographicRasterMetadataIn(**json_metadata)
    model_json = json.loads(model.json())
    del model_json["subjects"]
    del model_json["language"]
    del model_json["additional_metadata"]

    model_json["band_information"]["maximum_value"] = float(model_json["band_information"]["maximum_value"])
    model_json["band_information"]["minimum_value"] = float(model_json["band_information"]["minimum_value"])
    model_json["band_information"]["no_data_value"] = float(model_json["band_information"]["no_data_value"])

    assert json_metadata == model_json

def test_raster_single_extraction():
    json_metadata = _load_json("raster-single.json")
    del json_metadata["files"]
    model = GeographicRasterMetadataIn(**json_metadata)
    model_json = json.loads(model.json())
    del model_json["subjects"]
    del model_json["language"]
    del model_json["additional_metadata"]

    model_json["band_information"]["maximum_value"] = float(model_json["band_information"]["maximum_value"])
    model_json["band_information"]["minimum_value"] = float(model_json["band_information"]["minimum_value"])
    model_json["band_information"]["no_data_value"] = float(model_json["band_information"]["no_data_value"])

    assert json_metadata == model_json
'''
def test_features_watersheds_extraction():
    json_metadata = _load_json("feature.json")
    model = GeographicFeatureMetadata(**json_metadata)

    assert json.dumps(json_metadata, indent=2) == model.json(indent=2)

def test_reftimeseries_extraction():
    json_metadata = _load_json("reftimeseries.json")
    model = ReferencedTimeSeriesMetadata(**json_metadata)

    assert json.dumps(json_metadata, indent=2) == model.json(indent=2)

def test_timeseries_sqlite_extraction():
    json_metadata = _load_json("timeseries.json")
    model = TimeSeriesMetadata(**json_metadata)

    assert json.dumps(json_metadata, indent=2) == model.json(indent=2)

def test_timeseries_csv_extraction():
    json_metadata = _load_json("timeseries-csv.json")
    model = TimeSeriesMetadata(**json_metadata)

    assert json.dumps(json_metadata, indent=2) == model.json(indent=2)

def test_feature_states_extraction():
    json_metadata = _load_json("feature-states.json")
    model = GeographicFeatureMetadata(**json_metadata)

    assert json.dumps(json_metadata, indent=2) == model.json(indent=2)
'''