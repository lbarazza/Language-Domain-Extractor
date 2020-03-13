import re
from collections import Counter
import requests
from bs4 import BeautifulSoup


def freq(url, n=None):
    resp = requests.get(url)

    raw = ""
    if resp is not None:
        html = BeautifulSoup(resp.text, "html.parser")
        ps = html.select("p")
        for p in ps:
            raw += p.text.lower()

    text = re.sub('[^A-Za-z0-9]+', ' ', raw)
    terms = text.split()
    terms_dict = Counter(terms)

    sorted_terms = [i for i in reversed(sorted(terms_dict, key=terms_dict.get))]

    N = len(sorted_terms)
    if n:
        sorted_terms = sorted_terms[:n]

    return [(i+1, sorted_terms[i], terms_dict[sorted_terms[i]], terms_dict[sorted_terms[i]]/N) for i in range(len(sorted_terms))]

def compare_freq(x, base, k=1, n=None):
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


url1 = 'https://en.wikipedia.org/wiki/Physics'
#url1 = "https://it.wikipedia.org/wiki/Impressionismo"

terms_info1 = freq(url1)

#for term_info in terms_info1:
#    print('{:4d}. {:15}: {:5d}      freq.: {:5.3f}'.format(term_info[0], term_info[1], term_info[2], term_info[3]))

#print("-----------------------------------------------------------")

url2 = "https://en.wikipedia.org/wiki/English_language"#'https://en.wikipedia.org/wiki/Italy'
#url2 = "https://it.wikipedia.org/wiki/Italia"

terms_info2 = freq(url2)

#for term_info in terms_info2:
#    print('{:4d}. {:15}: {:5d}      freq.: {:5.3f}'.format(term_info[0], term_info[1], term_info[2], term_info[3]))

terms_info3 = compare_freq(terms_info1, terms_info2, k=1000, n=100)

print("+-----------------------+")
for term_info in terms_info3:
    print('| {:4d}. {:15} |'.format(term_info[0], term_info[1]))
print("+-----------------------+")
