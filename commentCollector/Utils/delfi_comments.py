from json.decoder import JSONDecodeError
from pprint import pprint
import requests
import unicodedata
import sys
from typing import List, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class Comment(TypedDict):
    id: int
    subject: str
    content: str


class CommentWithReplies(Comment):
    replies: List[Comment]


API_URL = "https://api.delfi.ee/comment/v1/graphql"
QUERY_PARENTS_REPLIES = """fragment CommentBody on Comment {
  id
  subject
  content
}

query cfe_getComments($articleId: Int!, $modeType: ModeType!, $offset: Int, $limit: Int, $orderBy: OrderBy, $limitReplies: Int, $orderByReplies: OrderBy, $lastCommentId: Int, $commentsBefore: Boolean) {
  getCommentsByArticleId(article_id: $articleId) {
    comments(mode_type: $modeType, offset: $offset, limit: $limit, orderBy: $orderBy) {
      ...CommentBody
      replies(lastCommentId: $lastCommentId, commentsBefore: $commentsBefore, limit: $limitReplies, orderBy: $orderByReplies) {
        ...CommentBody
      }
    }
  }
}
"""

QUERY_PARENTS_ONLY = """query cfe_getComments($articleId: Int!, $modeType: ModeType!, $offset: Int, $limit: Int, $orderBy: OrderBy) {
  getCommentsByArticleId(article_id: $articleId) {
    comments(mode_type: $modeType, offset: $offset, limit: $limit, orderBy: $orderBy) {
      id
      subject
      content
      count_replies
      count_registered_replies
    }
  }
}
"""


def get_comments_with_replies(article_id: int, anon=True, offset=0) -> List[CommentWithReplies]:
    return requests.post(
        API_URL,
        json={
            "operationName": "cfe_getComments",
            "variables": {
                "articleId": article_id,
                "modeType": "ANONYMOUS_MAIN" if anon else "REGISTERED_MAIN",
                "orderBy": "DATE_DESC",
                "offset": offset,
                "limit": 100,
                "limitReplies": 100,
                "orderByReplies": "DATE_DESC"
            },
            "query": QUERY_PARENTS_REPLIES,
        },
    ).json()["data"]["getCommentsByArticleId"]["comments"]


def get_comments(article_id: int, anon=True, offset=0) -> List[Comment]:
    try:
        return requests.post(
            API_URL,
            json={
                "operationName": "cfe_getComments",
                "variables": {
                    "articleId": article_id,
                    "modeType": "ANONYMOUS_MAIN" if anon else "REGISTERED_MAIN",
                    "orderBy": "DATE_DESC",
                    "offset": offset,
                    "limit": 100,
                },
                "query": QUERY_PARENTS_ONLY,
            },
        ).json()["data"]["getCommentsByArticleId"]["comments"]
    except (JSONDecodeError, requests.exceptions.ConnectionError) as e:
        print(f"Yeet {e}" )
        get_comments(article_id, anon, offset)



def get_all_comments(article_id: int, with_replies=False,
                     anon_reg=None) -> Union[List[Comment], List[CommentWithReplies]]:
    if anon_reg is None:
        anon_reg = [True, False]
    result = []
    for is_anon in anon_reg:
        has_more = True
        offset = 0
        while has_more:
            comments = get_comments_with_replies(article_id, is_anon, offset) \
                if with_replies \
                else get_comments(article_id, is_anon, offset)
            result += comments
            has_more = len(comments) > 99
            offset += 100

    return result


def normalize_text(text: str) -> str:
    if text:
        return unicodedata.normalize("NFKD", text)


def comment_to_string(comment: Comment) -> str:
    return "{}: {}".format(normalize_text(comment["subject"]), normalize_text(comment["content"]))


def flatten_comments(comments) -> Union[List[Comment], List[CommentWithReplies]]:
    content = []

    def append(comment):
        subject = normalize_text(comment["subject"])
        text = normalize_text(comment["content"])
        if subject and text:
            content.append((subject, text))

    for parent in comments:
        append(parent)
        if parent["replies"]:
            for reply in parent["replies"]:
                append(reply)

    return content


if __name__ == "__main__":
    res = get_comments_with_replies(89615287)
    pprint(res)
    print(len(res))
