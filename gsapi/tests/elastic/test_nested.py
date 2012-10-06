# -*- coding: utf-8 -*-
from __future__ import absolute_import
from gsapi.tests.esbase import ESTestCase, get_conn
from pyes.filters import TermFilter, NestedFilter
from pyes.query import FilteredQuery, MatchAllQuery, BoolQuery, TermQuery, PrefixQuery, WildcardQuery


from pyes import decode_json
#from pyes.mappings import Mapper

import time
class NestedSearchTestCase(ESTestCase):
    def setUp(self):
        super(NestedSearchTestCase, self).setUp()

        # self.conn = get_conn(timeout=300.0)
        # self.index_name = "test-index"
        # self.document_type = "test-type"

        # self.datamap = decode_json(self.get_datafile("map.json"))
        # _ = Mapper(self.datamap)

        if 1:
            mapping = {
                'shares': {
                    'type': 'nested'
                }
            }
            try:
                self.conn.create_index(self.index_name)
            except:
                pass
            self.conn.put_mapping(self.document_type, {'properties': mapping}, self.index_name)
            self.conn.index({"body": "hello",
                             "shares": [{"orgid": "abc.de.1",
                                          "role": "11"},
                                        {"orgid": "abc",
                                          "role": "1"}]},
                            self.index_name, self.document_type, 1)

            self.conn.index({"body": "world",
                             "shares": [{"orgid": "abc.de",
                                          "role": "111"}]},
                            self.index_name, self.document_type, 2)

            self.conn.index({"body": "today",
                             "shares": [{"orgid": "abc",
                                          "role": "111"}]},
                            self.index_name, self.document_type, 3)

            # self.conn.refresh(self.index_name)
            # a quicker way to see index change without doing refresh
            time.sleep(1)

    def test_nested_filter(self):


        q = FilteredQuery(MatchAllQuery(),
            NestedFilter('shares',
                BoolQuery(must=[PrefixQuery('shares.orgid', 'abc'),
                                PrefixQuery('shares.role', '11')])))
        resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        self.assertEquals(resultset.total, 3)
        print ', '.join([r['body'] for r in resultset])


        q = FilteredQuery(MatchAllQuery(),
            NestedFilter('shares',
                BoolQuery(must=[PrefixQuery('shares.orgid', 'abc.de'),
                                PrefixQuery('shares.role', '111')])))
        resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        self.assertEquals(resultset.total, 1)
        print ', '.join([r['body'] for r in resultset])



        q = FilteredQuery(MatchAllQuery(),
            NestedFilter('shares',
                BoolQuery(must=[PrefixQuery('shares.orgid', 'abc.de.1'),
                                PrefixQuery('shares.role', '11')])))
        resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        self.assertEquals(resultset.total, 0)
        print ', '.join([r['body'] for r in resultset])



        q = FilteredQuery(MatchAllQuery(),
            NestedFilter('shares',
                BoolQuery(must=[PrefixQuery('shares.orgid', 'abc'),
                                PrefixQuery('shares.role', '111')])))
        resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        self.assertEquals(resultset.total, 2)
        print ', '.join([r['body'] for r in resultset])


        print

        # q = FilteredQuery(MatchAllQuery(),
        #     TermFilter('_all', 'n_value1_1'))
        # resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        # self.assertEquals(resultset.total, 2)

        # q = FilteredQuery(MatchAllQuery(),
        #     TermFilter('nested1.n_field1', 'n_value1_1'))
        # resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        # self.assertEquals(resultset.total, 0)

        # q = FilteredQuery(MatchAllQuery(),
        #     TermFilter('nested1.n_field1', 'n_value1_1'))
        # resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        # self.assertEquals(resultset.total, 0)

        # q = FilteredQuery(MatchAllQuery(),
        #     NestedFilter('nested1',
        #         BoolQuery(must=[TermQuery('nested1.n_field1', 'n_value1_1')])))
        # resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        # self.assertEquals(resultset.total, 2)

        # q = FilteredQuery(MatchAllQuery(),
        #     NestedFilter('nested1',
        #         BoolQuery(must=[TermQuery('nested1.n_field1', 'n_value1_1'),
        #                         TermQuery('nested1.n_field2', 'n_value2_1')])))
        # resultset = self.conn.search(query=q, indices=self.index_name, doc_types=[self.document_type])
        # self.assertEquals(resultset.total, 1)


if __name__ == "__main__":
    unittest.main()

