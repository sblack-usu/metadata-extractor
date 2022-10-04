import pytest
import json

from hsextract.feature.utils import extract_metadata_and_files
from hsextract.raster.utils import extract_from_tif_file
from hsextract.netcdf.utils import get_nc_meta_dict
from hsextract.reftimeseries.utils import extract_referenced_timeseries_metadata
from hsextract.timeseries.utils import extract_metadata as extract_timeseries_metadata


def test_features_watersheds_extraction():
    metadata_dict = extract_metadata_and_files("tests/test_files/watersheds/watersheds.shp")
    metadata_json = json.loads(json.dumps(metadata_dict))

    with open("tests/outputs/feature.json", "r") as f:
        expected_str = f.read()
        expected_json = json.loads(expected_str)
    
    assert metadata_json == expected_json

def test_rasters_extraction():
    metadata_dict = extract_from_tif_file("tests/test_files/rasters/logan.vrt")
    metadata_json = json.loads(json.dumps(metadata_dict))
    

    with open("tests/outputs/raster.json", "r") as f:
        expected_str = f.read()
        expected_json = json.loads(expected_str)
    
    # remove the minimumValue, maximumValue and projection_string because gdal is inconsistent
    del metadata_json['_band_information_0']['maximumValue']
    del expected_json['_band_information_0']['maximumValue']

    del metadata_json['_band_information_0']['minimumValue']
    del expected_json['_band_information_0']['minimumValue']

    del metadata_json['_ori_coverage']['_value']['projection_string']
    del expected_json['_ori_coverage']['_value']['projection_string']

    assert metadata_json == expected_json

def test_netcdf_extraction():
    all_metadata_json, res_meta = get_nc_meta_dict("tests/test_files/netcdf/netcdf_valid.nc")
    all_metadata_json.update(res_meta)

    with open("tests/outputs/netcdf.json", "r") as f:
        expected_str = f.read()
        expected_json = json.loads(expected_str)

    assert all_metadata_json == expected_json

def test_reftimeseries_extraction():
    ref_timeseries_json = extract_referenced_timeseries_metadata("tests/test_files/reftimeseries/multi_sites_formatted_version1.0.refts.json")

    with open("tests/outputs/reftimeseries.json", "r") as f:
        expected_str = f.read()
        expected_json = json.loads(expected_str)

    assert ref_timeseries_json == expected_json

def test_timeseries_extraction():
    timeseries_json = extract_timeseries_metadata("tests/test_files/timeseries/ODM2_Multi_Site_One_Variable.sqlite")

    with open("tests/outputs/timeseries.json", "r") as f:
        expected_str = f.read()
        expected_json = json.loads(expected_str)

    assert timeseries_json == expected_json