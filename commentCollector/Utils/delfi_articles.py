import sys
import requests
from bs4 import BeautifulSoup
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class Article(TypedDict):
    id: int
    url: str
    name: str
    comments: int


ARTICLES_URL = "https://www.delfi.ee/"


def get_front_page_articles() -> List[Article]:
    page = requests.get(ARTICLES_URL)
    parser = BeautifulSoup(page.text, "html.parser")
    links_with_comments = parser.select(".headline a.headline__comments")
    articles: List[Article] = []
    for link in links_with_comments:
        title = link.find_previous_sibling("h1")
        if title and len(link["href"].split("?id=")) > 1:
            article = Article(
                id=int(link["href"].split("?id=")[1].replace("&com=1", "")),
                name=title.text,
                url=link["href"],
                comments=int(link.text.replace("(", "").replace(")", "")),
            )
            articles.append(article)

    return articles


def get_top_front_page_articles(limit=5) -> List[Article]:
    articles = get_front_page_articles()
    articles.sort(key=lambda x: x["comments"], reverse=True)
    return articles[:limit]


if __name__ == '__main__':
    print(get_top_front_page_articles())
