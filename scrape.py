# /usr/bin/env python
# coding: utf-8

'''
TODO: From/to page input options.
TODO: Database/file of successfully scraped urls to not scrape again.
'''

import bs4
import requests
from urlparse import urlparse, parse_qs
from time import sleep
from os.path import abspath, join as pathjoin, exists
from os import makedirs, stat
from itertools import chain
import re
import logging
import codecs
from urllib import urlencode
import sys
from optparse import OptionParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DEFAULT_SLEEP_TIME = 1  # seconds

first = lambda it: iter(it).next()


def fileize(s):
    return "".join((c for c in s if c.isalnum()))


def mkdirs(path):
    try:
        makedirs(path)
    except (OSError, WindowsError):
        pass

urlfile = pathjoin(abspath("."), "processed_urls.txt")


def load_processed_urls():
    """
    Suppport resume by not re-downloading already downloaded product pages.
    """
    if not exists(urlfile):
        return set()

    with codecs.open(urlfile, encoding='utf-8') as fp:
        return set(fp.read().splitlines())  # remove the n from the end


PROCESSED = load_processed_urls()


def save_processed_urls(urls):
    with codecs.open(urlfile, "w+", encoding="utf-8") as fp:
        fp.write(u"\n".join(list(urls)))


def record_data(title, description, taxonomy, pid, fname=None):
    """
    taxonomy: Hierarchical classification of product categories. From general
              to more specific.
              IE. [Category, Sub-Category, Sub-Sub-Category, ...]
    """
    base = pathjoin(abspath("."), "data", fileize(first(taxonomy)))
    mkdirs(base)
    if fname is None:
        fname = "{0}.txt".format(fileize(title))

    fpath = pathjoin(base, fname)
    logger.info(u"<record_data> Writing file: {0}".format(fpath))

    if exists(fpath):
        if stat(fpath).st_size == 0:
            logger.warn(u"<record_data> File already exists, but has no data. "
                        u"Continuing.")
        else:
            logger.warn(u"<record_data> File already exists with data. "
                        u"Skipping.")
            return

    with codecs.open(fpath, "w+", encoding="utf-8") as fp:
        lines = [
                u"{0}\n".format(u", ".join(taxonomy)),
                u"{0}\n".format(pid),
                u"{0}\n".format(title),
                u"{0}\n".format(description),
                ]
        #fp.writelines([l.encode("utf-8") for l in lines])
        fp.writelines(lines)


DIGIT_RE_C = re.compile(ur".*?(?P<pid>\d+).*")


def scrape_macys(murl, maxn=None):
    logger.info("Scraping Product Listing Page {url} for products."
            .format(url=murl))
    parsed = urlparse(murl)
    soup = bs4.BeautifulSoup(requests.get(murl).text)  # .content

    aelts = soup.select("div.shortDescription > a")
    product_hrefs = [a.get('href') for a in aelts]

    nscraped = 0
    for href in product_hrefs:
        if href is None:
            logger.warning("None entry found in href list.")
            continue

        if href in PROCESSED:
            logger.info("href already processed: {href}".format(href=href))
            continue

        logger.info("Scraping product page: {href}".format(href=href))

        fullhref = "{0}://{1}{2}".format(parsed.scheme, parsed.netloc, href)
        pdata = requests.get(fullhref)
        soup = bs4.BeautifulSoup(pdata.text)
        try:
            product_title = first(soup.select("#productTitle")).text
            product_ldesc = first(soup.select("#longDescription")).text

            listitems = soup.select("ul#bullets > li")
            product_ldesc = " ".join(chain((product_ldesc,),
                                     (li.text for li in listitems)))

            breadcrumbs = [a.text for a in soup.select(".breadCrumbs > a")]
            pid_text = first(soup.select(".productID")).text
            fname = fileize(product_title)

            try:
                pid = DIGIT_RE_C.match(pid_text).groupdict()['pid']
                fname += "_" + pid
            except AttributeError, attrerr:
                logger.warning("No product ID found")
                logger.error(str(attrerr))

            fname += ".txt"

            if all((product_title, product_ldesc, breadcrumbs)):
                record_data(product_title, product_ldesc, breadcrumbs, pid,
                            fname=fname)
            else:
                logger.warning("Did not record data for product url: {href}"
                        .format(href=href))
        except StopIteration:
            pass
        finally:
            PROCESSED.add(href)

        nscraped += 1
        if maxn is not None and nscraped >= maxn:
            break

        logger.debug("Sleeping {0} seconds".format(DEFAULT_SLEEP_TIME))
        sleep(DEFAULT_SLEEP_TIME)

    return nscraped


def configure_logging(filename="scrape.log"):
    root_logger = logging.getLogger()
    lsh = logging.StreamHandler()
    lfh = logging.FileHandler(filename)
    fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(module)s | %(message)s")
    lsh.setFormatter(fmt)
    lfh.setFormatter(fmt)
    root_logger.addHandler(lsh)
    root_logger.addHandler(lfh)
    root_logger.setLevel(logging.DEBUG)


def fix_chars(string):
    """
    Replace with punctuation that we will know to filter.

    TODO: Support full unicode punctuation in NLP pipeline.
    """
    # Replace lsquo (\x91)
    #fixed = re.sub(u"\x91", u"‘", string)
    fixed = re.sub(u"\x91", u"'", string)
    # Replace rsquo (\x92)
    #fixed = re.sub(u"\x92", u"’", fixed)
    fixed = re.sub(u"\x92", u"'", fixed)
    # Replace ldquo (\x93)
    #fixed = re.sub(u"\x93", u"“", fixed)
    fixed = re.sub(u"\x93", u'"', fixed)
    # Replace rdquo (\x94)
    #fixed = re.sub(u"\x94", u"”", fixed)
    fixed = re.sub(u"\x94", u'"', fixed)
    # Replace ndash (\x96)
    #fixed = re.sub(u"\x96", u"–", fixed)
    fixed = re.sub(u"\x96", u"-", fixed)
    # Replace mdash (\x97)
    #fixed = re.sub(u"\x97", u"—", fixed)
    fixed = re.sub(u"\x97", u"-", fixed)
    # Replace ellipsis char
    fixed = re.sub(u"\x85", u"...", fixed)
    return fixed


home_decor_url = \
    "http://www1.macys.com/shop/for-the-home/home-decor?id=55971&edge=hybrid"

all_bath_url = \
    "http://www1.macys.com/shop/bed-bath/shop-all-bath?id=8237&edge=hybrid"

all_fine_jewelery_url = \
    "http://www1.macys.com/shop/jewelry-watches/fine-jewelry?id=21996&edge=hybrid"

all_diamond_jewelery_url = \
    "http://www1.macys.com/shop/jewelry-watches/diamond-jewelry?id=67017&edge=hybrid"

sub_cat_url = ("http://www1.macys.com/catalog/index.ognc"
               "?CategoryID={catid}&pageIndex={pg}")

'''
http://www.macys.com/catalog/index.ognc?CategoryID=22672&cm_sp=us_hdr-_-homepage-_-22672_for-the-home

Each sub-category
http://www1.macys.com/shop/for-the-home/home-decor?id=55971&edge=hybrid

For each sub-sub-category
http://www1.macys.com/shop/for-the-home/bowls-vases?id=55973&edge=hybrid

Same thing, with pagination
http://www1.macys.com/catalog/index.ognc?CategoryID=55973&pageIndex=2
'''

P_CATS = ("home-decor", "bath", "fine-jewelery", "diamonds-jewelery")
P_URLS = (home_decor_url, all_bath_url, all_fine_jewelery_url,
        all_diamond_jewelery_url)
P_CAT_TO_URL = dict(zip(P_CATS, P_URLS))


def main():
    configure_logging()

    usage = ("%prog [list of catagories]")
    epilog = ('\nAvailable categories include: "{cats}". '
              "Specify \"all\" to scrape all categories.\n"
              "Examples:\n"
              "{prog} home-decor bath\n"
              "{prog} all\n"
              ).format(cats='", "'.join(P_CATS), prog=sys.argv[0])
    description="Macy's Product Scraper CLI."

    class MyParser(OptionParser):
        def format_epilog(self, formatter):
            return self.epilog

    parser = MyParser(usage=usage, description=description, epilog=epilog)

    (option, args) = parser.parse_args()

    # TODO: Replace with optparse
    if args[0] == "all":
        cats = P_CATS
    else:
        cats = set(P_CATS)
        for cat in args:
            if cat not in cats:
                parser.error("Invalid category specification.")
        cats = args

    for cat in cats:
        process_category(P_CAT_TO_URL[cat])


def process_category(url, max_scrape=20000):
    try:
        soup = bs4.BeautifulSoup(requests.get(url).text)
        main_parsed = urlparse(url)
        nscraped = 0

        # urls for sub-sub-category pages
        cat_urls = [a.attrs['href'] for a in soup.select("a.facet-item")]
        # each category url has an 'id' query parameter to use in the
        # CategoryID query parameter of the next url

        for cat_url in cat_urls:

            cat_parsed = urlparse(cat_url)
            if not cat_parsed.netloc:
                cat_href = "{0}://{1}{2}".format(main_parsed.scheme,
                                                main_parsed.netloc, cat_url)
            else:
                cat_href = cat_url

            cat_parsed = urlparse(cat_href)
            cat_qs = parse_qs(cat_parsed.query)

            #cat_href_1 = sub_cat_url.format(catid=first(cat_qs['id']), pg=1)
            cat_href_1 = cat_href

            soup = bs4.BeautifulSoup(requests.get(cat_href_1).text)

            nscraped_cat = 0
            # We already loaded the first page of items
            nscraped_cat += scrape_macys(cat_href_1)
            nscraped += nscraped_cat
            logger.info("Scraped {n} products so far".format(n=nscraped))

            # Discovery Category ID
            # <a href="http://www1.macys.com/catalog/index.ognc?CategoryID=55971
            # &amp;pageIndex=2">2</a>

            try:
                ahref = [a.attrs['href'] for a in soup.select("div.pagination > a")
                            if a.text.isnumeric()][0]
            except IndexError:
                # No pages
                continue

            m = re.match(ur".*?CategoryID=(\d+).*", ahref)
            catid = m.group(1)

            parentid = soup.select("div.parentCategories")[0].attrs['id']

            logger.info("Discovering the number of pages at url: {url}"
                        .format(url=cat_href_1))

            npages = max([int(pageno) for pageno in
                            [a.text for a in soup.select("div.pagination > a")]
                            if pageno.isnumeric()] or [0])

            logger.info("Number of pages found: {n}".format(n=npages))

            for page in range(2, npages+1):  # do the rest

                if nscraped_cat >= max_scrape:
                    break

                plisturl = (
                    "http://www1.macys.com/catalog/category/facetedmeta"
                    "?edge=hybrid&"
                    "parentCategoryId={parentid}&"
                    "categoryId={catid}&"
                    "multifacet=true&"
                    "pageIndex={pg}&"
                    "sortBy=ORIGINAL&"
                    "productsPerPage=40&")

                product_ids = requests.get(plisturl
                        .format(parentid=parentid, catid=catid, pg=page))\
                        .json()['productIds']

                pageurl = (
                    "http://www1.macys.com/shop/catalog/product/thumbnail/1?"
                    "edge=hybrid&limit=none&suppressColorSwatches=false&"
                    "categoryId={catid}&"
                    "ids={ids}")

                # `ids` is a comma-separated list of <parentid>_<itemid> strings.
                # The top level product page uses this ajax request to continue
                # to request details of more products (pagination).

                ids = ",".join(["_".join((str(catid), str(pid)))
                                    for pid in product_ids])
                nscraped_cat += scrape_macys(
                        pageurl.format(catid=catid, ids=ids))
                nscraped += nscraped_cat

                logger.info("Scraped {n} products so far".format(n=nscraped))

        logger.info("Scraping Complete")

    finally:
        save_processed_urls(PROCESSED)

if __name__ == "__main__":
    main()


        #logger.error("Valid categories: " + ", ".join(P_CATS + ("all",)))
        #sys.exit(1)
