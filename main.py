import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Ok")


app = webapp2.WSGIApplication([('/', MainPage)],
        debug=True)
