#!/usr/bin/env pytest
###############################################################################
# $Id$
#
# Project:  GDAL/OGR Test Suite
# Purpose:  Test TileDB driver vector functionality.
# Author:   Even Rouault <even dot rouault at spatialys dot com>
#
###############################################################################
# Copyright (c) 2023, Even Rouault <even dot rouault at spatialys dot com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################

import json
import os
import shutil

import gdaltest
import pytest
import test_cli_utilities

from osgeo import gdal, ogr, osr

pytestmark = pytest.mark.require_driver("TileDB")


###############################################################################


@pytest.mark.parametrize("nullable,batch_size", [(True, None), (False, 2)])
def test_ogr_tiledb_basic(nullable, batch_size):

    if os.path.exists("tmp/test.tiledb"):
        shutil.rmtree("tmp/test.tiledb")

    ds = ogr.GetDriverByName("TileDB").CreateDataSource("tmp/test.tiledb")
    srs = osr.SpatialReference()
    srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    srs.ImportFromEPSG(4326)
    options = []
    if batch_size:
        options += ["BATCH_SIZE=" + str(batch_size)]
    lyr = ds.CreateLayer("test", srs=srs, options=options)

    fld_defn = ogr.FieldDefn("strfield", ogr.OFTString)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("intfield", ogr.OFTInteger)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("int16field", ogr.OFTInteger)
    fld_defn.SetNullable(nullable)
    fld_defn.SetSubType(ogr.OFSTInt16)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("boolfield", ogr.OFTInteger)
    fld_defn.SetNullable(nullable)
    fld_defn.SetSubType(ogr.OFSTBoolean)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("int64field", ogr.OFTInteger64)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("doublefield", ogr.OFTReal)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("floatfield", ogr.OFTReal)
    fld_defn.SetNullable(nullable)
    fld_defn.SetSubType(ogr.OFSTFloat32)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("binaryfield", ogr.OFTBinary)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("intlistfield", ogr.OFTIntegerList)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("int16listfield", ogr.OFTIntegerList)
    fld_defn.SetNullable(nullable)
    fld_defn.SetSubType(ogr.OFSTInt16)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("boollistfield", ogr.OFTIntegerList)
    fld_defn.SetNullable(nullable)
    fld_defn.SetSubType(ogr.OFSTBoolean)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("doublelistfield", ogr.OFTRealList)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("floatlistfield", ogr.OFTRealList)
    fld_defn.SetNullable(nullable)
    fld_defn.SetSubType(ogr.OFSTFloat32)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("datetimefield", ogr.OFTDateTime)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("datefield", ogr.OFTDate)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("timefield", ogr.OFTTime)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    fld_defn = ogr.FieldDefn("intfieldextra", ogr.OFTInteger)
    fld_defn.SetNullable(nullable)
    lyr.CreateField(fld_defn)

    field_count = lyr.GetLayerDefn().GetFieldCount()

    f = ogr.Feature(lyr.GetLayerDefn())
    f["strfield"] = "foo"
    f["intfield"] = -123456789
    f["int16field"] = -32768
    f["boolfield"] = True
    f["int64field"] = -1234567890123456
    f["doublefield"] = 1.2345
    f["floatfield"] = 1.5
    f.SetFieldBinaryFromHexString("binaryfield", "DEADBEEF")
    f["intlistfield"] = [-123456789, 123]
    f["int16listfield"] = [-32768, 32767]
    f["boollistfield"] = [True, False]
    f["doublelistfield"] = [1.2345, -1.2345]
    f["floatlistfield"] = [1.5, -1.5, 0]
    f["datetimefield"] = "2023-04-07T12:34:56.789Z"
    f["datefield"] = "2023-04-07"
    f["timefield"] = "12:34:56.789"
    f["intfieldextra"] = 1
    f.SetGeometry(ogr.CreateGeometryFromWkt("POLYGON ((1 2,1 3,4 3,1 2))"))
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    assert f.GetFID() == 1

    f = ogr.Feature(lyr.GetLayerDefn())
    f["intfieldextra"] = 2
    f.SetGeometry(ogr.CreateGeometryFromWkt("POLYGON ((1 2,1 3,4 3,1 2))"))
    if not nullable:
        with gdaltest.error_handler():
            assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    else:
        assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    assert f.GetFID() == 2

    f = ogr.Feature(lyr.GetLayerDefn())
    f["strfield"] = "barbaz"
    f["intfield"] = 123456789
    f["int16field"] = 32767
    f["boolfield"] = False
    f["int64field"] = 1234567890123456
    f["doublefield"] = -1.2345
    f["floatfield"] = -1.5
    f.SetFieldBinaryFromHexString("binaryfield", "BEEFDEAD")
    f["intlistfield"] = [123456789, -123]
    f["int16listfield"] = [32767, -32768]
    f["boollistfield"] = [False, True]
    f["doublelistfield"] = [-1.2345, 1.2345]
    f["floatlistfield"] = [0.0, -1.5, 1.5]
    # Will be transformed to "2023/04/07 10:19:56.789+00"
    f["datetimefield"] = "2023-04-07T12:34:56.789+0215"
    f["datefield"] = "2023-04-08"
    f["timefield"] = "13:34:56.789"
    f["intfieldextra"] = 3
    f.SetGeometry(ogr.CreateGeometryFromWkt("POLYGON ((-1 -2,-1 -3,-4 -3,-1 -2))"))
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    assert f.GetFID() == 3

    ds = None

    ds = gdal.OpenEx("tmp/test.tiledb", open_options=options)
    lyr = ds.GetLayer(0)
    assert lyr.GetGeomType() == ogr.wkbUnknown
    assert lyr.GetSpatialRef().IsSame(srs)
    assert lyr.GetFeatureCount() == 3
    assert lyr.GetExtent() == (-4.0, 4.0, -3.0, 3.0)
    assert lyr.GetLayerDefn().GetFieldCount() == field_count
    for i in range(field_count):
        assert lyr.GetLayerDefn().GetFieldDefn(i).IsNullable() == nullable

    for i in range(3):
        f = lyr.GetNextFeature()
        if f.GetFID() == 1:
            assert f["strfield"] == "foo"
            assert f["intfield"] == -123456789
            assert f["int16field"] == -32768
            assert f["boolfield"] == True
            assert f["int64field"] == -1234567890123456
            assert f["doublefield"] == 1.2345
            assert f["floatfield"] == 1.5
            assert f.GetFieldAsBinary("binaryfield") == b"\xde\xad\xbe\xef"
            assert f["intlistfield"] == [-123456789, 123]
            assert f["int16listfield"] == [-32768, 32767]
            assert f["boollistfield"] == [True, False]
            assert f["doublelistfield"] == [1.2345, -1.2345]
            assert f["floatlistfield"] == [1.5, -1.5, 0]
            assert f["datetimefield"] == "2023/04/07 12:34:56.789+00"
            assert f["datefield"] == "2023/04/07"
            assert f["timefield"] == "12:34:56.789"
            assert f.GetGeometryRef().ExportToWkt() == "POLYGON ((1 2,1 3,4 3,1 2))"
        elif f.GetFID() == 2:
            assert f["intfieldextra"] == 2
            if nullable:
                for i in range(field_count):
                    if lyr.GetLayerDefn().GetFieldDefn(i).GetName() != "intfieldextra":
                        assert f.IsFieldNull(i)
            else:
                for i in range(field_count):
                    assert not f.IsFieldNull(i)
            assert f.GetGeometryRef().ExportToWkt() == "POLYGON ((1 2,1 3,4 3,1 2))"
        elif f.GetFID() == 3:
            assert f["strfield"] == "barbaz"
            assert f["intfield"] == 123456789
            assert f["int16field"] == 32767
            assert f["boolfield"] == False
            assert f["int64field"] == 1234567890123456
            assert f["doublefield"] == -1.2345
            assert f["floatfield"] == -1.5
            assert f.GetFieldAsBinary("binaryfield") == b"\xbe\xef\xde\xad"
            assert f["intlistfield"] == [123456789, -123]
            assert f["int16listfield"] == [32767, -32768]
            assert f["boollistfield"] == [False, True]
            assert f["doublelistfield"] == [-1.2345, 1.2345]
            assert f["floatlistfield"] == [0.0, -1.5, 1.5]
            assert f["datetimefield"] == "2023/04/07 10:19:56.789+00"
            assert f["datefield"] == "2023/04/08"
            assert f["timefield"] == "13:34:56.789"
            assert (
                f.GetGeometryRef().ExportToWkt()
                == "POLYGON ((-1 -2,-1 -3,-4 -3,-1 -2))"
            )
        else:
            assert False

    f = lyr.GetNextFeature()
    assert f is None

    f = lyr.GetFeature(0)
    assert f is None

    f = lyr.GetFeature(3)
    assert f.GetFID() == 3
    assert f["strfield"] == "barbaz"

    lyr.SetSpatialFilterRect(0, 0, 10, 10)
    assert lyr.GetFeatureCount() == 2
    assert set(f.GetFID() for f in lyr) == set([1, 2])

    f = lyr.GetFeature(3)
    assert f.GetFID() == 3
    assert f["strfield"] == "barbaz"

    lyr.SetSpatialFilterRect(-10, -10, 0, 0)
    assert lyr.GetFeatureCount() == 1
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetSpatialFilterRect(100, 100, 110, 110)
    assert lyr.GetFeatureCount() == 0
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetSpatialFilter(None)

    lyr.SetAttributeFilter("strfield = 'foo'")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("'foo' = strfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("strfield = 'non_existing'")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("strfield <> 'foo'")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    res = set(f.GetFID() for f in lyr)
    assert 3 in res
    assert 1 not in res

    lyr.SetAttributeFilter("'foo' <> strfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    res = set(f.GetFID() for f in lyr)
    assert 3 in res
    assert 1 not in res

    lyr.SetAttributeFilter("intfield = -123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("intfield = -123456789.0")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("intfield = -9876543")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("intfield >= 123456790")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("123456790 <= intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("intfield >= 123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetAttributeFilter("123456789 <= intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetAttributeFilter("intfield > 123456788")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetAttributeFilter("123456788 < intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetAttributeFilter("intfield > 123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("123456789 < intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("intfield < -123456788")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("-123456788 > intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("-123456788 > intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("intfield < -123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("-123456789 > intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("intfield <= -123456790")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("-123456790 >= intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("intfield <= -123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("-123456789 >= intfield")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("boolfield = 1")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("boolfield = 0")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([3]) if nullable else set([2, 3]))

    # Out of domain
    lyr.SetAttributeFilter("boolfield = 2")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("boolfield <> 2")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    # Out of domain
    lyr.SetAttributeFilter("int16field = -32769")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("int16field <> -32769")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("int16field > -32769")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("int16field >= -32769")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("int16field < -32769")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("int16field <= -32769")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("int16field = 32768")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("int16field <> 32768")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("int16field < 32768")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("int16field <= 32768")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("int16field > 32768")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("int16field >= 32768")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("int64field = 1234567890123456")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetAttributeFilter("int64field = 1234567890123456.0")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetAttributeFilter("int64field > 2000000000")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([3])

    lyr.SetAttributeFilter("doublefield = 1.2345")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("doublefield = 1.2345999")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("doublefield = 1")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("floatfield = 1.5")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("datetimefield = '2023-04-07T12:34:56.789Z'")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    with pytest.raises(Exception):
        assert lyr.SetAttributeFilter("datetimefield = 'invalid'") == ogr.OGRERR_FAILURE

    lyr.SetAttributeFilter("datefield = '2023-04-07'")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    with pytest.raises(Exception):
        assert lyr.SetAttributeFilter("datefield = 'invalid'") == ogr.OGRERR_FAILURE

    lyr.SetAttributeFilter("timefield = '12:34:56.789'")
    # timefield comparison not supported by tiledb currently
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "NONE"
    assert set(f.GetFID() for f in lyr) == set([1])

    # Test AND
    lyr.SetAttributeFilter("int16field = -32768 AND intfield = -123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("int16field = 0 AND intfield = -123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("intfield = -123456789 AND int16field = 0")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set([])

    lyr.SetAttributeFilter("intfield = -123456789 AND (1 = 1)")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "PARTIAL"
    assert set(f.GetFID() for f in lyr) == set([1])

    lyr.SetAttributeFilter("(1 = 1) AND intfield = -123456789")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "PARTIAL"
    assert set(f.GetFID() for f in lyr) == set([1])

    # Test OR
    has_working_or_filter = (
        gdal.GetDriverByName("TileDB").GetMetadataItem("HAS_TILEDB_WORKING_OR_FILTER")
        != "NO"
    )
    if has_working_or_filter:
        lyr.SetAttributeFilter("intfield = 321 OR intfield = -123456789")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1])

        lyr.SetAttributeFilter("intfield = -123456789 OR intfield = 321")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1])

        lyr.SetAttributeFilter("intfield = 321 OR intfield = 123")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([])

        lyr.SetAttributeFilter("(1 = 1) OR intfield = -123456789")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "NONE"
        assert set(f.GetFID() for f in lyr) == set([1, 2, 3])

        lyr.SetAttributeFilter("(1 = 0) OR intfield = -123456789")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "NONE"
        assert set(f.GetFID() for f in lyr) == set([1])

        lyr.SetAttributeFilter("intfield = -123456789 OR (1 = 1)")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "NONE"
        assert set(f.GetFID() for f in lyr) == set([1, 2, 3])

        lyr.SetAttributeFilter("intfield = -123456789 OR (1 = 0)")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "NONE"
        assert set(f.GetFID() for f in lyr) == set([1])

    # Test NOT
    lyr.SetAttributeFilter("NOT (intfield = -123456789)")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([3]) if nullable else set([2, 3]))

    # Test IN
    if has_working_or_filter:
        lyr.SetAttributeFilter("intfield IN (321, -123456789)")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1])

        lyr.SetAttributeFilter("intfield IN (-123456789, 321)")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1])

    # Test IS NULL / IS NOT NULL
    lyr.SetAttributeFilter("strfield IS NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

    lyr.SetAttributeFilter("strfield IS NOT NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("intfield IS NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

    lyr.SetAttributeFilter("intfield IS NOT NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    # Test IS NULL and AND (for always_false situations)

    lyr.SetAttributeFilter("intfield IS NULL AND intfieldextra <> 4")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

    lyr.SetAttributeFilter("intfield IS NULL AND intfield IS NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

    lyr.SetAttributeFilter("intfieldextra <> 4 AND intfield IS NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

    lyr.SetAttributeFilter("intfield IS NULL AND intfieldextra = 4")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("intfieldextra = 4 AND intfield IS NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    # Test IS NOT NULL and AND (for always_true situations)

    lyr.SetAttributeFilter("intfield IS NOT NULL AND intfieldextra <> 4")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("intfield IS NOT NULL AND intfield IS NOT NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("intfieldextra <> 4 AND intfield IS NOT NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == (set([1, 3]) if nullable else set([1, 2, 3]))

    lyr.SetAttributeFilter("intfield IS NOT NULL AND intfieldextra = 4")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    lyr.SetAttributeFilter("intfieldextra = 4 AND intfield IS NOT NULL")
    assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
    assert set(f.GetFID() for f in lyr) == set()

    # Test IS NULL and OR (for always_false situations)
    if has_working_or_filter:
        lyr.SetAttributeFilter("intfield IS NULL OR intfieldextra <> 4")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1, 2, 3])

        lyr.SetAttributeFilter("intfield IS NULL OR intfield IS NULL")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

        lyr.SetAttributeFilter("intfieldextra <> 4 OR intfield IS NULL")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1, 2, 3])

        lyr.SetAttributeFilter("intfield IS NULL OR intfieldextra = 4")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

        lyr.SetAttributeFilter("intfieldextra = 4 OR intfield IS NULL")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == (set([2]) if nullable else set())

    # Test IS NOT NULL and OR (for always_true situations)
    if has_working_or_filter:
        lyr.SetAttributeFilter("intfield IS NOT NULL OR intfieldextra <> 4")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1, 2, 3])

        lyr.SetAttributeFilter("intfield IS NOT NULL OR intfield IS NOT NULL")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == (
            set([1, 3]) if nullable else set([1, 2, 3])
        )

        lyr.SetAttributeFilter("intfieldextra <> 4 OR intfield IS NOT NULL")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == set([1, 2, 3])

        lyr.SetAttributeFilter("intfield IS NOT NULL OR intfieldextra = 4")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == (
            set([1, 3]) if nullable else set([1, 2, 3])
        )

        lyr.SetAttributeFilter("intfieldextra = 4 OR intfield IS NOT NULL")
        assert lyr.GetMetadataItem("ATTRIBUTE_FILTER_TRANSLATION", "_DEBUG_") == "WHOLE"
        assert set(f.GetFID() for f in lyr) == (
            set([1, 3]) if nullable else set([1, 2, 3])
        )

    tiledb_md = json.loads(lyr.GetMetadata_List("json:TILEDB")[0])
    md = tiledb_md["array"]["metadata"]
    del md["CRS"]
    assert md == {
        "FEATURE_COUNT": {"type": "INT64", "value": 3},
        "FID_ATTRIBUTE_NAME": {"type": "STRING_UTF8", "value": "FID"},
        "GEOMETRY_ATTRIBUTE_NAME": {"type": "STRING_UTF8", "value": "wkb_geometry"},
        "GeometryType": {"type": "STRING_ASCII", "value": "Unknown"},
        "LAYER_EXTENT_MAXX": {"type": "FLOAT64", "value": 4.0},
        "LAYER_EXTENT_MAXY": {"type": "FLOAT64", "value": 3.0},
        "LAYER_EXTENT_MINX": {"type": "FLOAT64", "value": -4.0},
        "LAYER_EXTENT_MINY": {"type": "FLOAT64", "value": -3.0},
        "PAD_X": {"type": "FLOAT64", "value": 1.5},
        "PAD_Y": {"type": "FLOAT64", "value": 0.5},
    }

    ds = None

    shutil.rmtree("tmp/test.tiledb")


###############################################################################


@pytest.mark.parametrize(
    "wkt",
    [
        "POINT (1 2)",
        "POINT Z (1 2 3)",
        "POINT M (1 2 3)",
        "POINT ZM (1 2 3 4)",
        "LINESTRING (1 2,3 4)",
        "POLYGON ((0 0,0 1,1 1,0 0))",
        "MULTIPOINT ((0 0))",
        "MULTILINESTRING ((1 2,3 4))",
        "MULTIPOLYGON (((0 0,0 1,1 1,0 0)))",
        "GEOMETRYCOLLECTION (POINT (1 2))",
        "CIRCULARSTRING (0 0,1 1,2 0)",
        "COMPOUNDCURVE ((1 2,3 4))",
        "CURVEPOLYGON ((0 0,0 1,1 1,0 0))",
        "MULTICURVE ((1 2,3 4))",
        "MULTISURFACE (((0 0,0 1,1 1,0 0)))",
        "POLYHEDRALSURFACE (((0 0,0 1,1 1,0 0)))",
        "TIN (((0 0,0 1,1 1,0 0)))",
    ],
)
def test_ogr_tiledb_geometry_types(wkt):

    if os.path.exists("tmp/test.tiledb"):
        shutil.rmtree("tmp/test.tiledb")

    g = ogr.CreateGeometryFromWkt(wkt)
    ds = ogr.GetDriverByName("TileDB").CreateDataSource("tmp/test.tiledb")
    options = ["BOUNDS=-1e4,-1e4,1e4,1e4"]
    if g.GetGeometryType() in (ogr.wkbPoint, ogr.wkbPoint25D):
        options += ["GEOMETRY_NAME="]
    lyr = ds.CreateLayer("test", geom_type=g.GetGeometryType(), options=options)
    f = ogr.Feature(lyr.GetLayerDefn())
    f.SetGeometry(g)
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    ds = None

    ds = ogr.Open("tmp/test.tiledb")
    lyr = ds.GetLayer(0)
    assert lyr.GetGeomType() == g.GetGeometryType()
    if g.GetGeometryType() in (ogr.wkbPoint, ogr.wkbPoint25D):
        assert lyr.GetGeometryColumn() == ""
    else:
        assert lyr.GetGeometryColumn() == "wkb_geometry"
    f = lyr.GetNextFeature()
    assert f.GetGeometryRef().ExportToIsoWkt() == wkt
    ds = None

    shutil.rmtree("tmp/test.tiledb")


###############################################################################


def test_ogr_tiledb_compression():

    if os.path.exists("tmp/test.tiledb"):
        shutil.rmtree("tmp/test.tiledb")

    ds = ogr.GetDriverByName("TileDB").CreateDataSource("tmp/test.tiledb")
    lyr = ds.CreateLayer(
        "test", options=["BOUNDS=-1e4,-1e4,1e4,1e4", "COMPRESSION=ZSTD"]
    )
    for (typ, subtype) in [
        (ogr.OFTInteger, ogr.OFSTNone),
        (ogr.OFTInteger, ogr.OFSTBoolean),
        (ogr.OFTInteger, ogr.OFSTInt16),
        (ogr.OFTReal, ogr.OFSTNone),
        (ogr.OFTReal, ogr.OFSTFloat32),
        (ogr.OFTInteger64, ogr.OFSTNone),
        (ogr.OFTIntegerList, ogr.OFSTNone),
        (ogr.OFTIntegerList, ogr.OFSTBoolean),
        (ogr.OFTIntegerList, ogr.OFSTInt16),
        (ogr.OFTRealList, ogr.OFSTNone),
        (ogr.OFTRealList, ogr.OFSTFloat32),
        (ogr.OFTInteger64List, ogr.OFSTNone),
        (ogr.OFTString, ogr.OFSTNone),
        (ogr.OFTBinary, ogr.OFSTNone),
        (ogr.OFTTime, ogr.OFSTNone),
        (ogr.OFTDate, ogr.OFSTNone),
        (ogr.OFTDateTime, ogr.OFSTNone),
    ]:
        fld_defn = ogr.FieldDefn("field%d_subtype%d" % (typ, subtype), typ)
        fld_defn.SetSubType(subtype)
        lyr.CreateField(fld_defn)
    ds = None

    ds = ogr.Open("tmp/test.tiledb")
    lyr = ds.GetLayer(0)
    tiledb_md = json.loads(lyr.GetMetadata_List("json:TILEDB")[0])
    ds = None

    assert tiledb_md["schema"]["coords_filter_list"] == ["ZSTD"]
    for attr in tiledb_md["schema"]["attributes"]:
        assert attr["filter_list"] == ["ZSTD"], attr

    shutil.rmtree("tmp/test.tiledb")


###############################################################################
# Run test_ogrsf


@pytest.mark.skipif(
    test_cli_utilities.get_test_ogrsf_path() is None, reason="test_ogrsf not available"
)
def test_ogr_tiledb_test_ogrsf():

    if os.path.exists("tmp/poly.tiledb"):
        shutil.rmtree("tmp/poly.tiledb")

    gdal.VectorTranslate("tmp/poly.tiledb", "data/poly.shp", format="TileDB")

    ret = gdaltest.runexternal(
        test_cli_utilities.get_test_ogrsf_path() + " tmp/poly.tiledb"
    )

    shutil.rmtree("tmp/poly.tiledb")

    assert "INFO" in ret
    assert "ERROR" not in ret


###############################################################################


def test_ogr_tiledb_dimension_names_open_option():

    if os.path.exists("tmp/test.tiledb"):
        shutil.rmtree("tmp/test.tiledb")

    ds = ogr.GetDriverByName("TileDB").CreateDataSource("tmp/test.tiledb")
    lyr = ds.CreateLayer(
        "test",
        geom_type=ogr.wkbPoint,
        options=["BOUNDS=-1e4,-1e4,1e4,1e4", "FID=", "GEOMETRY_NAME="],
    )
    f = ogr.Feature(lyr.GetLayerDefn())
    f.SetGeometry(ogr.CreateGeometryFromWkt("POINT (1 2)"))
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    ds = None

    ds = ogr.Open("tmp/test.tiledb")
    lyr = ds.GetLayer(0)
    f = lyr.GetNextFeature()
    assert f.GetGeometryRef().ExportToIsoWkt() == "POINT (1 2)"
    ds = None

    ds = gdal.OpenEx("tmp/test.tiledb", open_options=["DIM_X=_Y", "DIM_Y=_X"])
    lyr = ds.GetLayer(0)
    f = lyr.GetNextFeature()
    assert f.GetGeometryRef().ExportToIsoWkt() == "POINT (2 1)"
    ds = None

    shutil.rmtree("tmp/test.tiledb")


###############################################################################


def test_ogr_tiledb_switch_between_read_and_write():

    if os.path.exists("tmp/test.tiledb"):
        shutil.rmtree("tmp/test.tiledb")

    ds = ogr.GetDriverByName("TileDB").CreateDataSource("tmp/test.tiledb")
    lyr = ds.CreateLayer("test", options=["BOUNDS=-1e4,-1e4,1e4,1e4"])
    lyr.ResetReading()
    assert lyr.TestCapability(ogr.OLCSequentialWrite)
    assert lyr.TestCapability(ogr.OLCCreateField)
    assert lyr.CreateField(ogr.FieldDefn("intfield", ogr.OFTInteger)) == ogr.OGRERR_NONE
    f = ogr.Feature(lyr.GetLayerDefn())
    f["intfield"] = 1
    f.SetGeometry(ogr.CreateGeometryFromWkt("POINT (1 2)"))
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    assert f.GetFID() == 1

    assert lyr.TestCapability(ogr.OLCCreateField) == 0
    with pytest.raises(Exception):
        assert (
            lyr.CreateField(ogr.FieldDefn("intfield2", ogr.OFTInteger))
            == ogr.OGRERR_FAILURE
        )

    f = ogr.Feature(lyr.GetLayerDefn())
    f["intfield"] = 2
    f.SetGeometry(ogr.CreateGeometryFromWkt("POINT (2 3)"))
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    assert f.GetFID() == 2

    lyr.ResetReading()
    f = lyr.GetNextFeature()
    assert f.GetFID() == 1

    f = ogr.Feature(lyr.GetLayerDefn())
    f["intfield"] = 3
    f.SetGeometry(ogr.CreateGeometryFromWkt("POINT (3 4)"))
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    assert f.GetFID() == 3

    f = lyr.GetNextFeature()
    assert f.GetFID() == 1

    f = lyr.GetNextFeature()
    assert f.GetFID() == 2

    f = lyr.GetNextFeature()
    assert f.GetFID() == 3

    f = lyr.GetNextFeature()
    assert f is None

    ds = None

    ds = ogr.Open("tmp/test.tiledb", update=1)
    lyr = ds.GetLayer(0)
    assert lyr.TestCapability(ogr.OLCSequentialWrite)
    assert lyr.GetFeatureCount() == 3

    f = ogr.Feature(lyr.GetLayerDefn())
    f["intfield"] = 4
    f.SetGeometry(ogr.CreateGeometryFromWkt("POINT (4 5)"))
    assert lyr.CreateFeature(f) == ogr.OGRERR_NONE
    assert f.GetFID() == 4

    f = lyr.GetNextFeature()
    assert f.GetFID() == 1

    f = lyr.GetNextFeature()
    assert f.GetFID() == 2

    f = lyr.GetNextFeature()
    assert f.GetFID() == 3

    f = lyr.GetNextFeature()
    assert f.GetFID() == 4

    f = lyr.GetNextFeature()
    assert f is None

    ds = None

    shutil.rmtree("tmp/test.tiledb")


###############################################################################


def test_ogr_tiledb_create_group():

    if "CREATE_GROUP" not in gdal.GetDriverByName("TileDB").GetMetadataItem(
        gdal.DMD_CREATIONOPTIONLIST
    ):
        pytest.skip("CREATE_GROUP not supported in TileDB < 2.9")

    if os.path.exists("tmp/test.tiledb"):
        shutil.rmtree("tmp/test.tiledb")

    ds = ogr.GetDriverByName("TileDB").CreateDataSource(
        "tmp/test.tiledb", options=["CREATE_GROUP=YES"]
    )
    assert ds.TestCapability(ogr.ODsCCreateLayer)
    lyr = ds.CreateLayer("test", options=["BOUNDS=-1e4,-1e4,1e4,1e4"])
    lyr.CreateField(ogr.FieldDefn("field", ogr.OFTString))
    assert ds.TestCapability(ogr.ODsCCreateLayer)
    lyr2 = ds.CreateLayer("test2", options=["BOUNDS=-1e4,-1e4,1e4,1e4"])
    lyr2.CreateField(ogr.FieldDefn("field2", ogr.OFTString))
    ds = None

    assert os.path.exists("tmp/test.tiledb/layers/test")
    assert os.path.exists("tmp/test.tiledb/layers/test2")

    ds = ogr.Open("tmp/test.tiledb")
    assert ds.GetLayerCount() == 2
    lyr = ds.GetLayerByName("test")
    assert lyr
    assert lyr.GetLayerDefn().GetFieldDefn(0).GetName() == "field"
    lyr = ds.GetLayerByName("test2")
    assert lyr
    assert lyr.GetLayerDefn().GetFieldDefn(0).GetName() == "field2"

    # Cannot create layer: read-only connection
    assert ds.TestCapability(ogr.ODsCCreateLayer) == 0
    with pytest.raises(Exception):
        ds.CreateLayer("failed", options=["BOUNDS=-1e4,-1e4,1e4,1e4"])
    ds = None

    ds = ogr.Open("tmp/test.tiledb", update=1)
    assert ds.TestCapability(ogr.ODsCCreateLayer)
    lyr = ds.CreateLayer("test/3", options=["BOUNDS=-1e4,-1e4,1e4,1e4"])
    assert lyr
    ds = None

    assert os.path.exists("tmp/test.tiledb/layers/test/3")

    ds = ogr.Open("tmp/test.tiledb")
    assert ds.GetLayerCount() == 3
    lyr = ds.GetLayerByName("test/3")
    assert lyr
    ds = None

    shutil.rmtree("tmp/test.tiledb")


###############################################################################


def test_ogr_tiledb_errors():

    if os.path.exists("tmp/test.tiledb"):
        shutil.rmtree("tmp/test.tiledb")

    ds = ogr.GetDriverByName("TileDB").CreateDataSource("tmp/test.tiledb")

    with pytest.raises(Exception):
        ds.CreateLayer("test", geom_type=ogr.wkbNone)

    with pytest.raises(Exception):
        ds.CreateLayer("test")  # missing bounds

    with pytest.raises(Exception):
        ds.CreateLayer("test", options=["BOUNDS=invalid"])

    lyr = ds.CreateLayer("test", options=["BOUNDS=1,2,3,4,5,6", "ADD_Z_DIM=YES"])

    with pytest.raises(Exception):
        ds.CreateLayer("another_layer", options=["BOUNDS=1,2,3,4,5,6"])

    lyr.CreateField(ogr.FieldDefn("foo", ogr.OFTString))
    for field_name in ("FID", "wkb_geometry", "_X", "_Y", "_Z", "foo"):
        # Existing field name
        with pytest.raises(Exception):
            lyr.CreateField(ogr.FieldDefn("FID", ogr.OFTString))

    with pytest.raises(Exception):
        # feature without geom
        lyr.CreateFeature(ogr.Feature(lyr.GetLayerDefn()))

    # feature with empty geom
    f = ogr.Feature(lyr.GetLayerDefn())
    f.SetGeometry(ogr.Geometry(ogr.wkbPoint))
    with pytest.raises(Exception):
        lyr.CreateFeature(f)
    ds = None

    shutil.rmtree("tmp/test.tiledb")
