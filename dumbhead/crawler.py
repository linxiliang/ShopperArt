from pyquery import PyQuery as pq
import requests

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/37.0.2062.120 Safari/537.36'}

PURL = 'https://www.amazon.com/dp/B0074703CM/'


def get_data(url):
    con = pq(requests.get(url, headers=headers).text)
    pid = url.rsplit('/')[-2]
    title = con('#productTitle').text()
    price = con('#priceblock_ourprice').text()
    desc = []
    for item in con('#feature-bullets .a-list-item'):
        desc.append(con(item).text())
    reviews = get_reviews(pid)
    return dict(pid=pid, title=title, price=price, desc=desc, reviews=reviews)


def get_reviews(pid):
    url = 'https://www.amazon.com/product-reviews/{pid}/'.format(pid=pid)
    con = pq(requests.get(url, headers=headers).text)
    reviews = []
    for review in con('#cm_cr-review_list .review-text'):
        reviews.append(con(review).text())
    return reviews



