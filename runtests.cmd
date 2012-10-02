REM All
nosetests -s

REM nosetests -v gsapi/tests/usecases/test_usecases_initial.py
REM nosetests -v gsapi.tests.controllers.test_generic

REM nosetests -v gsapi.tests.test_elastic_pyes:TestESPyes.test_index_sample_data
REM nosetests -v gsapi.tests.test_elastic_pyes:TestESPyes

REM nosetests -v --nocapture gsapi.tests.test_generic:TestGeneric.test_post_one

REM nosetests -v --nocapture gsapi.tests.test_contacts:TestPersons.test_patch

REM By name
REM nosetests -v --nocapture gsapi.tests.test_contacts:TestPersons.test_find