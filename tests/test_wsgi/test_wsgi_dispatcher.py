# -*- encoding: UTF-8 -*-

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response

from mongorest.testcase import TestCase
from mongorest.wsgi import WSGIWrapper, WSGIDispatcher


class TestWSGIWrapper(TestCase):

    def test_wsgi_dispatcher_init_returns_werkzeug_app_with_mounted_resources(self):
        class WSGIWrapperTest(WSGIWrapper):
            endpoint = 'test'
            url_map = Map([Rule('/', methods=['GET'], endpoint='test')])

            def test(self, request):
                return Response(status=999)

        app = WSGIDispatcher([WSGIWrapperTest])
        self.assertEqual(list(app.mounts.keys()), ['/test'])
