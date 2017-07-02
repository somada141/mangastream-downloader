# mangastream-downloader

This is a simple collection of scripts that allows one to download a [MangaStream](http://mangastream.com/) manga chapter by providing the URL to the first page of the chapter.

The script scrapes the HTML source of the page, retrieves the link to the current image as well as the URL that image points to, i.e., the next page of the chapter. It then saves every page image into an in-memory zip-file and continues this process until the end of the chapter.

## Usage

The `mangastream.py` module acts as a CLI interface to the code under `scraper.py` and can be used to either download a single chapter from a provided URL or all chapters appearing in the [MangaStream RSS Feed](http://mangastream.com/rss).

Download a single chapter through its URL and write it to a `.zip` file:

    python mangastream.py url http://mangastream.com/r/neverland/010/3728/1 neverland_010.zip

Download all chapters under the [http://mangastream.com/rss](http://mangastream.com/rss) RSS feed and write them under the `./chapters` directory:

    mkdir chapters_rss
    python mangastream.py rss ./chapters_rss

### Docker

A `Dockerfile` is provided, configured so that the chapters under MangaStream RSS can be downloaded through scheduled jobs at regular intervals and stored under a shared volume. The execution of an image tagged `mangastream-downloader:latest` can be performed as follows:

    docker run --rm -v /some/host/directory:/tmp/mangastream_downloader mangastream-downloader:latest

where the `/some/host/directory` host directory is mapped to `/tmp/mangastream_downloader` in the container where the downloaded chapters will be stored. This directory also serves as a cache, as chapters found under that directory will not be re-downloaded.

## Underlying behaviour

A few notes regarding this script's operation:

- [MangaStream](http://mangastream.com/) tends to name its page images not only by order but by the version they released at the time. As a result, the image for the 5th page may be named `005.jpg` or `0053.jpg` if they released the 3rd version. This convention tends to mess up the order of the files and precludes the chapter being read correctly through a `.zip` archive. As such, the pages are written with the correct extension but numbered simply by the order in which they're seen.

