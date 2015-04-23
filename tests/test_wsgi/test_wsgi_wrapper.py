# -*- encoding: UTF-8 -*-

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIWrapper, WSGIDispatcher


class TestWSGIWrapper(TestCase):

    def test_wsgi_wrapper_executes_correct_view_if_url_exists_on_map(self):
        class WSGIWrapperTest(WSGIWrapper):
            url_map = Map([Rule('/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher([WSGIWrapperTest])
        response = self.client(app, Response).get('/')

        self.assertEqual(response.status_code, 999)
