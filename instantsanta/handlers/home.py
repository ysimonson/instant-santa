import os
import cv2
import base
import numpy
import hashlib
from instantsanta import engine
from tornado import web, gen, httpclient

static_path = lambda path: "./static/%s" % path

class ImageHandler(base.BaseHandler):
    @web.asynchronous
    @gen.engine
    def get(self, url):
        path = "generated/%s.jpg" % hashlib.sha256(url).hexdigest()

        if not os.path.exists(static_path(path)):
            http_client = httpclient.AsyncHTTPClient()
            response = yield http_client.fetch(url)

            if response.code == 404:
                raise web.HTTPError(404)
            elif response.code != 200:
                raise web.HTTPError(400)

            if not os.path.exists(static_path(path)):
                np_array = numpy.fromstring(response.body, numpy.uint8)
                img = cv2.imdecode(np_array, cv2.CV_LOAD_IMAGE_COLOR)
                rects = engine.detect(img)
                img = engine.santas(rects, img)
                cv2.imwrite(static_path(path), img)

        self.redirect(self.static_url(path))

class HomeHandler(base.BaseHandler):
    def get_file_body(self, name):
        """Gets the contents of an uploaded file by its argument name"""
        f = self.request.files.get(name)
        return f[0]["body"] if f else None

    def get(self):
        return self.render("index.html", error=None, img=None)

    def post(self):
        contents = self.get_file_body("file")

        if not contents:
            return self.render("index.html", img="")

        path = "saved/%s.jpg" % hashlib.sha256(contents).hexdigest()

        with open(static_path(path), "wb") as f:
            f.write(contents)

        self.render("index.html", img="/image/%s" % self.static_url(path, include_host=True))
