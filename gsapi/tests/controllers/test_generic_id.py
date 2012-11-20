# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA

import os
from gsapi.tests.base import TestCase
import json
import time
from gsapi import models
from gsapi import controllers

class TestGenericId(TestCase):
    print "Generic tests id"
    print "=============="
    generic   = controllers.Generic(self.db)
    genericId = controllers.GenericId(self.db)

    def test_no_existing_class(self):
        print
        print "Where these is no existing model class Id's"
        print "^^^^^^^^^^^"

        response = self.genericId.nextId('Cnt')

        assert response['status_code'] == 200
        assert response['nextId'] == 1

    def test_existing_class(self):
        print
        print "Where there is an existing model class with max id 4"
        print "^^^^^^^^^^^"

        sample_docs = [{
            "_c": "Prs", "id": 1,
        }, {
            "_c": "Prs", "id": 2,
        }, {
            "_c": "Prs", "id": 3,
        }, {
            "_c": "Prs", "id": 4,
        }]

        args = {}
        args['class_name'] = 'Id'
        args['docs'] = sample_docs

        # add some test ids
        response = generic.post(**args)

        response = self.genericId.nextId('Prs')

        assert response['status_code'] == 200
        assert response['nextId'] == 5


if __name__ == "__main__":
    unittest.main()
