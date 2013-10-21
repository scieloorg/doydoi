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

    callback = request.POST.get('callback', None)
    callback_id = request.POST.get('callback_id', None)
    query_data = request.POST.get('data', None)

    if not all([callback, callback_id, query_data]):
        raise HTTPBadRequest()

    try:
        qry = Query(callback_url=callback,
                    callback_id=callback_id,
                    query_data=query_data)
        DBSession.add(qry)
    except DBAPIError:
        pass
    else:
        return HTTPFound({'status': 'ok'})

