
import logging

import requests
import bs4

import utils

logging.basicConfig()
logger = logging.getLogger("mangastream")
logger.setLevel("DEBUG")


def get_url_image(soup_page):
    div_page = soup_page.find("div", attrs={"class": "page"})

    if not div_page:
        return None

    url_image = div_page.find("img", attrs={"id": "manga-page"})["src"]

    return url_image


def get_url_next(soup_page):
    div_page = soup_page.find("div", attrs={"class": "page"})

    if not div_page:
        return None

    url_next = div_page.find("a")["href"]

    return url_next


def get_chapter(url_chapter):

    url_next = url_chapter

    # create an in-memory zip-file to store the retrieved images
    fzip = utils.InMemoryZip()

    counter_page = 1
    while True:
        logger.info("Getting page '{0}'".format(url_next))

        # get the page and parse it with `BeautifulSoup`
        response = requests.get(url_next)
        soup_page = bs4.BeautifulSoup(response.content, "html5lib")

        # retrieve the image URL
        url_image = get_url_image(soup_page=soup_page)

        # stop if no image was found
        if not url_image:
            break

        logger.info("Getting image '{0}'".format(url_image))

        # retrieve the actual image
        response_image = requests.get(url_image)
        
        content_type = response_image.headers["Content-Type"]
        image_extension = content_type.split("/")[-1]

        # retrieve the last bit of the URL and use it as the image filename
        # fname_image = os.path.basename(url_image)
        fname_image = "{0}.{1}".format(str(counter_page).zfill(3), image_extension)

        logger.info("Saving image '{0}'".format(fname_image))

        # write the retrieved image into the in-memory zip-file
        fzip = fzip.append(fname_image, response_image.content)

        # get the next URL
        url_next_candidate = get_url_next(soup_page=soup_page)

        # if anything but the last bit of the URL has changed that means we were redirected to the next chapter
        # instead of the next image so halt execution
        if url_next.split("/")[-2] != url_next_candidate.split("/")[-2]:
            break
        else:
            url_next = url_next_candidate

        counter_page += 1

    # return the in-memory zip-file
    return fzip
