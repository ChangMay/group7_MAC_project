import requests
from bs4 import BeautifulSoup
import re
import os
import pickle

def create_strings_from_wikipedia(maximum_length, count, lang):
    """
        Create all string by randomly picking Wikipedia articles and taking sentences from them.
    """
    sentences = []

    while len(sentences) < count:
        # print(len(sentences))
        # We fetch a random page

        page_url = "https://{}.wikipedia.org/wiki/Special:Random".format(lang)
        try:
            page = requests.get(page_url, timeout=3.0)  # take into account timeouts
        except requests.exceptions.Timeout:
            continue

        soup = BeautifulSoup(page.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        # Only take a certain length
        lines = list(
            filter(
                lambda s: len(s.split(" ")) < maximum_length and len(s.split(" ")) > 1
                          and not "Wikipedia" in s
                          and not "wikipedia" in s,
                [
                    " ".join(re.findall(r"[\w']+", s.strip()))[0:200]
                    for s in soup.get_text().splitlines()
                ],
            )
        )

        # Remove the last lines that talks about contributing
        sentences.extend(lines[0: max([1, len(lines) - 5])])

    return sentences[0:count]
    
dictionary = None
if './dictionary/dict_sorted.pkl' in os.listdir('./'):
    with open('dictionary/dict_sorted.pkl', 'rb') as f:
        dictionary = pickle.load(f)

# print(dictionary)

if dictionary == None:
    dictionary = {}
string_list = create_strings_from_wikipedia(10, 15000, 'en')
print('string_list:', len(string_list))

with open('dictionary/dict_sorted.pkl', 'wb') as f:
    for string in string_list:
        words = string.split()
        # print(words)
        for word in words:
          if word.isdigit():
              # print('digit!!!!!')
              continue
          if word[-1] == '.' or word[-1] == ',':
              word = word[:-1]
              
          if word in dictionary.keys():
              dictionary[word] += 1
          else:
              dictionary[word] = 1
    
    items = dictionary.items()
    items = list(items)
    items.sort(key=lambda k: len(k[0]))
    del dictionary
    dictionary = {}
    for k, v in items:
        dictionary[k] = v
    
    pickle.dump(dictionary, f)
    print('dictionary:', len(dictionary))
