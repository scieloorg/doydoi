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


class CrossRefBrokerTests(unittest.TestCase):

    @unittest.skip('not implemented')
    def test_search(self):
        from .crossrefbroker import search
        from .domain import Article
        self.assertRaises(ValueError, lambda: search(Article))


class ArticleReferenceTests(unittest.TestCase):

    def test_init_from_json(self):
        article_sample = """
        {"author": "Jim Gettys and Phil Karlton and Scott McGregor",
          "title": "The {X} Window System, Version 11",
          "journal": "Software Practice and Experience",
          "volume": "20",
          "number": "52",
          "year": "1990"}
        """
        from .domain import Article
        article = Article.from_json(article_sample)

        self.assertEquals(article.author, "Jim Gettys and Phil Karlton and Scott McGregor")
        self.assertEquals(article.title, "The {X} Window System, Version 11")
        self.assertEquals(article.journal, "Software Practice and Experience")
        self.assertEquals(article.volume, "20")
        self.assertEquals(article.number, "52")
        self.assertEquals(article.year, "1990")

    def test_missing_raises_TypeError(self):
        from .domain import Article
        self.assertRaises(TypeError, lambda: Article(author='Foo'))

    def test_missing_data_is_informed(self):
        from .domain import Article
        try:
            Article()
        except TypeError as e:
            self.assertIn('author', e.message)
            self.assertIn('title', e.message)
            self.assertIn('journal', e.message)
            self.assertIn('volume', e.message)
            self.assertIn('number', e.message)
            self.assertIn('year', e.message)

    def test_values_are_coerced_to_unicode(self):
        from .domain import Article
        article = Article(author='Foo', title='Bar', journal='Baz',
            volume=20, number=52, year=1990)

        self.assertIsInstance(article.author, basestring)
        self.assertIsInstance(article.title, basestring)
        self.assertIsInstance(article.journal, basestring)
        self.assertIsInstance(article.volume, basestring)
        self.assertIsInstance(article.number, basestring)
        self.assertIsInstance(article.year, basestring)

