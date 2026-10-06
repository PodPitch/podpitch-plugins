import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / 'references' / 'catalog.json'
STOP_WORDS = set('a an and are as at be by for from how i in is it me my of on or podcast podcasts show shows that the to with'.split())


def words(text):
    return [word for word in re.findall(r'\w+', text.casefold()) if word not in STOP_WORDS]


def search(catalog, query, limit):
    query_words = set(words(query))
    documents = [(podcast, Counter(words(podcast['title'] + ' ' + podcast['description'] + ' ' + podcast['category'])))
                 for podcast in catalog['podcasts']]
    frequencies = Counter(word for _, counts in documents for word in query_words if word in counts)
    ranked = []
    for podcast, counts in documents:
        score = sum((1 + math.log(counts[word])) * math.log(1 + len(documents) / (1 + frequencies[word]))
                    for word in query_words if word in counts)
        if score:
            title_words = set(words(podcast['title']))
            score += sum(2 for word in query_words if word in title_words)
            ranked.append((score, podcast))
    ranked.sort(key=lambda row: (-row[0], row[1]['id']))
    return [podcast for _, podcast in ranked[:limit]]


def main():
    parser = argparse.ArgumentParser(description='Search the bundled public PodPitch snapshot without network access.')
    parser.add_argument('query', nargs='?')
    parser.add_argument('--limit', type=int, choices=range(1, 11), default=3)
    parser.add_argument('--id')
    args = parser.parse_args()
    if not args.id and (not args.query or not words(args.query)):
        parser.error('Provide a topic, show name, or --id returned by search.')
    catalog = json.loads(CATALOG.read_text())
    podcasts = ([podcast for podcast in catalog['podcasts'] if podcast['id'] == args.id]
                if args.id else search(catalog, args.query, args.limit))
    print(json.dumps({'source': catalog['source'], 'captured_at': catalog['captured_at'],
                      'is_live': False, 'is_complete_catalog': False, 'podcasts': podcasts}, ensure_ascii=False))


if __name__ == '__main__':
    main()
