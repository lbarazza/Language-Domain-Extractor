import re
from collections import Counter
import requests
from bs4 import BeautifulSoup
from pattern3.text.en import singularize


def freq(urls, n=None):

    raw = ""
    for url in urls:
        resp = requests.get(url)

        if resp is not None:
            html = BeautifulSoup(resp.text, "html.parser")
            ps = html.select("p")
            for p in ps:
                raw += p.text.lower()

    text = re.sub('[^A-Za-z0-9ا-ي]+', ' ', raw)
    terms = text.split()
    for i in range(len(terms)):
        terms[i] = singularize(terms[i])
    terms_dict = Counter(terms)

    sorted_terms = [i for i in reversed(sorted(terms_dict, key=terms_dict.get))]

    N = len(sorted_terms)
    if n:
        sorted_terms = sorted_terms[:n]

    return [(i+1, sorted_terms[i], terms_dict[sorted_terms[i]], terms_dict[sorted_terms[i]]/N) for i in range(len(sorted_terms))]

def compare_freq(x, base, n=None, k=1):
    x_ = {}
    for i in x:
        x_[i[1]] = i[3]

    base_ = {}
    for i in base:
        base_[i[1]] = i[3]

    y_ = {}
    for key, value in x_.items():
        y_[key] = value - k*(base_[key] if key in base_ else 0)

    y = [i for i in reversed(sorted(y_, key=y_.get))]
    z = [(i+1, y[i]) for i in range(len(y))]
    if n:
        z = z[:n]
    return z


url1 = "https://ar.wikipedia.org/wiki/%D8%B9%D9%84%D9%85_%D8%A7%D9%84%D9%86%D8%A8%D8%A7%D8%AA"#'https://en.wikipedia.org/wiki/Mathematics'
#url1 = "https://it.wikipedia.org/wiki/Impressionismo"

terms_info1 = freq([url1])

url_base1 = "https://en.wikipedia.org/wiki/English_language"
url_base2 = 'https://en.wikipedia.org/wiki/Italy'
#url_base2 = "https://it.wikipedia.org/wiki/Italia"

#base1 = freq(url_base1)
#base2 = freq(url_base2)
#base = set(base1 + base2)

base_epochs = 50
url_base = "https://ar.wikipedia.org/wiki/Special:Random"
base = []

base = freq([url_base] * base_epochs)

terms_info3 = compare_freq(terms_info1, base, n=50, k=100)

print("+----------------------------+")
for term_info in terms_info3:
    print('| {:4d}. {:20} |'.format(term_info[0], term_info[1]))
print("+----------------------------+")
