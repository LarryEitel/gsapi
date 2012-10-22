# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import re
import json
from gsapi.utils import preparse_json_doc


class TestUtils(unittest.TestCase):
    def test_datetime(self):
        '''Test inputs and outputs of datetimes.
        Client may submit datetimes in the following formats:
            # How it appears in Mongo Shell and MongoVue
            2011-12-17T13:10:33.987Z :UTC
            2011-12-17T07:10:33.987-06:00 :Local
            1324127433.987 : Local

        ElasticSearch
            http://www.elasticsearch.org/guide/reference/mapping/date-format.html
            
        '''

    def test_parse_json(self):
        ''' MongoVue of a doc
        {
            "_id"   : ObjectId("50536c4c2558712e205a269a"),
            "mBy"   : ObjectId("50468de92558713d84b03fd7"),
            "dOn"   : ISODate("2012-09-14T23:00:00Z"),
            "dOn"   : { "$date" : 1347644492471 },
            "dOn"   : { "$date" : 1347644492.471 },
            "prefix" : "president",
            "oOn"   : ISODate("2012-09-14T11:41:32Z"),
            "shares": [],
            "mOn"   : ISODate("2012-09-14T11:41:32Z"),
            "fNam"  : "nam1",
            "oBy"   : ObjectId("50468de92558713d84b03fd7"),
            "cBy"   : ObjectId("50468de92558713d84b03fd7"),
            "_c"    : "Prs",
            "emails": [],
            "cOn"   : ISODate("2012-09-14T11:41:32Z")
            }
            '''

        print "\nTestUtils.test_parse_json"

        sample_json = '''
        { "_id" : { "$oid" : "50536c4c2558712e205a269a" },
        "mBy" : { "$oid" : "50468de92558713d84b03fd7" },
        "mBy" : ObjectId("50536c4c2558792f205a299d"),
        "prefix" : "president",
        "oOn" : { "$date" : 1347644492471 },
        "dOn" : { "$date" : 1347644492.471 },
        "shares" : [],
        "mOn" : { "$date" : 1347644492400 },
        "mOn" : ISODate("2012-09-14T17:41:32.471Z"),
        "mOn" : "$isodate:2012-09-14T17:41:32.471Z",
        "fNam" : "nam1",
        "oBy" : { "$oid" : "50468de92558713d84b03fd7" },
        "cBy" : { "$oid" : "50468de92558713d84b03fd7" },
        "_c" : "Prs", "emails" : [],
        "cOn" : { "$date" : 1347644492471 } }
        '''

        expected_result = '''
        { "_id" : "$oid:50536c4c2558712e205a269a",
        "mBy" : "$oid:50468de92558713d84b03fd7",
        "mBy" : "$oid:50536c4c2558792f205a299d",
        "prefix" : "president",
        "oOn" : "$date:1347644492471",
        "dOn" : "$date:1347644492471",
        "shares" : [],
        "mOn" : "$date:1347644492400",
        "mOn" : "$isodate:2012-09-14T17:41:32.471Z",
        "mOn" : "$isodate:2012-09-14T17:41:32.471Z",
        "fNam" : "nam1",
        "oBy" : "$oid:50468de92558713d84b03fd7",
        "cBy" : "$oid:50468de92558713d84b03fd7",
        "_c" : "Prs", "emails" : [],
        "cOn" : "$date:1347644492471" }
        '''
        ret = preparse_json_doc(sample_json)
        assert ret == expected_result






if __name__ == "__main__":
    unittest.main()
