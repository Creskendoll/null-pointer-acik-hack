from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.getData = False
        self.found = ""

    # class="mw-search-result-heading"
    def handle_starttag(self, tag, attrs):
        self.getData = False
        if tag == "a":
            for attr in attrs:
                if attr[0] == "data-serp-pos" and attr[1] == "0":
                    self.getData = True
                    print("attr:", attr)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.getData and self.found == "" and data != "\\n" and data != " " and data != "\n":
            self.found = data
            print("DATA", data)