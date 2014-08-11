#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import sys
import re, urlparse

# Source: http://stackoverflow.com/a/4391299
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

# Source: http://stackoverflow.com/a/4391299
def iriToUri(iri):
    parts = urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna')
        if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

#==============================================================================
# autocompleteQuery()
#==============================================================================
def autocompleteQuery(query):
    client = "firefox"
    language = "el"
    url = "http://suggestqueries.google.com/complete/search?client=" + client \
            + "&q=" + query + "&hl=" + language
    iri = iriToUri(url)
    escaped_iri = urllib2.quote(iri, safe="%/:=&?~#+!$,;'@()*[]")
    result = urllib2.urlopen(escaped_iri).read().decode('iso8859-7')
    return result.split("[")[2].split("]]")[0].split(",")

#==============================================================================
# main()
#==============================================================================
def main():
    if (len(sys.argv) != 2):
        print "Syntax:", sys.argv[0], "<query>"
        sys.exit(1)

    query = unicode(sys.argv[1], 'utf-8')
    results = autocompleteQuery(query)
    for r in results:
        print r[1:-1] # strip first and last quotes

if __name__ == "__main__":
    main()
