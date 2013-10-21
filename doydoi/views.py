from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Query,
    )


@view_config(route_name='new_doi_query', renderer='json', request_method='POST')
def new_doi_query(request):

    callback, query_data = request.POST.get('callback', None), request.POST.get('data', None)
    if callback is None or query_data is None:
        raise HTTPBadRequest()

    try:
        qry = Query(callback_url=callback, query_data=query_data)
        DBSession.add(qry)
    except DBAPIError:
        pass
    else:
        return HTTPFound({'status': 'ok'})

