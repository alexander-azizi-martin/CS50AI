import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}

    if len(corpus[page]) == 0:
        for key in corpus:
            distribution[key] = 1 / len(corpus)

        return distribution

    for key in corpus:
        distribution[key] = (1 - damping_factor) / len(corpus)

        if key in corpus[page]:
            distribution[key] += damping_factor / len(corpus[page])

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))
    step = 1 / n

    for i in range(n):
        page_ranks[current_page] += step
        transition = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            list(transition.keys()), list(transition.values()))[0]

    print(sum(page_ranks.values()))

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {key: 1 / len(corpus) for key in corpus}
    difference = False

    while not difference:
        for page in page_ranks:
            new_page_rank = (1 - damping_factor) / len(corpus)
            links = get_links(page, corpus)

            for link in links:
                new_page_rank += damping_factor * \
                    (page_ranks[link] / len(corpus[link]))

            # new_page_rank *= damping_factor

            # if len(corpus[page]) == 0:
            #     new_page_rank += damping_factor / len(corpus)

            if abs(page_ranks[page] - new_page_rank) < 0.001 :
                difference = True
            else:
                difference = False

            page_ranks[page] = new_page_rank

    print(sum(page_ranks.values()))

    return page_ranks


def get_links(page, corpus):
    """
    Return a list of pages that link to page.
    """
    links = []

    for key in corpus:
        if page in corpus[key]:
            links.append(key)

    return links


if __name__ == "__main__":
    main()
