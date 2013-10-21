import json


class Article(object):
    def __init__(self, author=None, title=None, journal=None,
                 volume=None, number=None, year=None):

        missing = [key for key, val in locals().items() if val is None]
        if missing:
            raise TypeError('None is not an accepted value for %s.' % ', '.join(missing))

        self.author = unicode(author)
        self.title = unicode(title)
        self.journal = unicode(journal)
        self.volume = unicode(volume)
        self.number = unicode(number)
        self.year = unicode(year)


    @classmethod
    def from_json(cls, data):
        py_data = json.loads(data)
        return cls(author=py_data['author'],
                   title=py_data['title'],
                   journal=py_data['journal'],
                   volume=py_data['volume'],
                   number=py_data['number'],
                   year=py_data['year'])

