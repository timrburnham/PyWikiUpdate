import mwclient
import re
from glob import glob
from os.path import basename, splitext


def update_page(wikiname, wikibasepath, pagename, username, password, contents):
    site = mwclient.Site(('http', wikiname), wikibasepath, force_login=True)
    site.login(username, password)
    page = site.Pages[pagename]

    if page.exists:
        section_title = re.search(r'^== *([^=\n]*?) *==$', contents, re.M).group(1)
        print('update_page: found text {}'.format(section_title))
        sec = get_section(page, section_title)
        if sec: # section already exists
            print()
            page.save(contents, section=sec)
        else: # append new section to end of page
            pagetext = page.text()
            pagetext += '\n\n' + contents
            page.save(pagetext)
    else: # page doesn't exist yet
        page.save(contents)

def get_section(page, section_title):
    site = page.site
    title = page.page_title
    parse = site.parse(page=title, prop='sections')
    for section in parse['sections']:
        if section['line'] == section_title:
            return int(section['index'])


def main():
    wikiname = "localhost"
    wikibasepath = "/w/"
    #pagename = "User:Tim"
    username = "tim"
    password = "hotstuff"

    for f in glob("logs/*"):
        print("opening file: {}".format(f))
        with open(f, 'r') as file:
            pagename = splitext(basename(f))[0]
            contents = file.read()
            update_page(wikiname, wikibasepath, pagename, username, password, contents)


if __name__ == "__main__":
    main()
    
