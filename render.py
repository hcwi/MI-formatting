from StringIO import StringIO

import yaml
import sys


def render_attr(attr):
    buffer = StringIO()
    if attr.get("required", False):
        req = "*"
    else:
        req = ""
    if attr.get("specific for", False):
       buffer.write("<span title=\"Specific for {}\">{}{}</span>".format(
               attr["specific for"], attr["name"], req))
    else:
        buffer.write("{}{}".format(attr["name"], req))
    children = attr.get("children", [])
    if children:
        buffer.write("\n<ul>\n")
        for ch in children:
            buffer.write("<li>\n")
            buffer.write(render_attr(ch))
            buffer.write("</li>\n")
        buffer.write("</ul>")
    return buffer.getvalue()


def render_sl(sl):
    return """<a href="{ref}">{name}</a>""".format(**sl)

def render_ont(ont):
    if ont.get("abbr", False):
        abbr = ", {}".format(ont["abbr"])
    else:
        abbr = ""
    return """<a href="{}">{}{}</a>""".format(ont["ref"], ont["name"], abbr)

def render_html(doc):
    buffer = StringIO()
    buffer.write("<tr>\n")

    buffer.write("<td>{}</td>\n".format(doc["section name"]))

    buffer.write("<td><ul>\n")
    for attr in doc["attributes"]:
        buffer.write("<li>{}</li>\n".format(render_attr(attr)))
    buffer.write("</ul></td>")

    buffer.write("<td><ul>")
    for sl in doc["source list"]:
        buffer.write("<li>{0}</li>\n".format(render_sl(sl)))
    buffer.write("</ul></td>\n")

    buffer.write("<td><ul>")
    for ont in doc["recommended ontologies"]:
        buffer.write("<li>{0}</li>\n".format(render_ont(ont)))
    buffer.write("</ul></td>\n")

    buffer.write("</tr>")

    return buffer.getvalue()


def main(filename):
    f = open(filename, "r"):
    docs = yaml.load(f)
    print "<table style='border-collapse:collapse;'>"
    print "<tr>" \
          "<th>Section</th>" \
          "<th>Attributes</th>" \
          "<th>Source list</th>" \
          "<th>Recommended ontologies</th>" \
          "</tr>"
    for doc in docs["sections"]:
        print render_html(doc)
    print "</table>"

if __name__=='__main__':
    main(sys.argv[1])
