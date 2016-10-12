
import os
import logging
import begin
import feedparser

import scraper


@begin.subcommand
@begin.tracebacks
@begin.logging
def url(url, fname_output):
    fzip = scraper.get_chapter(url_chapter=url)
    fzip.writetofile(fname_output)


@begin.subcommand
@begin.tracebacks
@begin.logging
def rss(path, overwrite=False, url_rss="https://mangastream.com/rss"):
    if not os.path.exists(path) or not os.path.isdir(path):
        raise ValueError("Invalid output path '{0}'".format(path))

    rss = feedparser.parse(url_rss)

    for entry in rss["entries"]:
        title = entry["title"]
        url = entry["link"]

        fname_output = os.path.join(path, "{0}.zip".format(title))
        if os.path.exists(fname_output):
            continue

        fzip = scraper.get_chapter(url_chapter=url)
        fzip.writetofile(fname_output)


@begin.start
def main():
    pass
