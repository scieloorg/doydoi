import unittest
import transaction

from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound

from .models import DBSession


class TestNewDoiQuery(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            Query,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_missing_returns_400(self):
        from .views import new_doi_query
        request = testing.DummyRequest()

        self.assertRaises(HTTPBadRequest, lambda: new_doi_query(request))

    def test_missing_callback_returns_400(self):
        from .views import new_doi_query
        request = testing.DummyRequest()
        request.POST = {'data': '{"foo": "baz"}'}

        self.assertRaises(HTTPBadRequest, lambda: new_doi_query(request))

    def test_missing_callback_id_returns_400(self):
        from .views import new_doi_query
        request = testing.DummyRequest()
        request.POST = {'data': '{"foo": "baz"}',
                        'callback': 'http://foo.com/bar/'}

        self.assertRaises(HTTPBadRequest, lambda: new_doi_query(request))

    def test_missing_data_returns_400(self):
        from .views import new_doi_query
        request = testing.DummyRequest()
        request.POST = {'callback': 'http://foo.com/bar/'}

        self.assertRaises(HTTPBadRequest, lambda: new_doi_query(request))

    def test_new_doi_query(self):
        from .views import new_doi_query
        from .models import Query
        request = testing.DummyRequest()
        request.POST = {'callback': 'http://foo.com/bar/',
                        'callback_id': '1234',
                        'data': '{"foo": "baz"}'}

        self.assertIsInstance(new_doi_query(request), HTTPFound)
        record = DBSession.query(Query).one()
        self.assertEquals(record.callback_url, u'http://foo.com/bar/')
        self.assertEquals(record.callback_id, '1234')
        self.assertEquals(record.query_data, '{"foo": "baz"}')

