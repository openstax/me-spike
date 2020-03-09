class Request:
    def __init__(self, data):
        self.data = data
        self.headers = data['headers']

    def country_code(self):
        viewer_country_header = self.headers.get('cloudfront-viewer-country')
        if viewer_country_header:
            return viewer_country_header[0]['value']
        else:
            return None

    def path(self):
        return self.data.get('uri')

    def parsedCookies(self):
        parsedCookie = {}
        if self.headers.get('cookie'):
            for cookie in self.headers['cookie'][0]['value'].split(';'):
                if cookie:
                    parts = cookie.split('=')
                    parsedCookie[parts[0].strip()] = parts[1].strip()
        return parsedCookie
