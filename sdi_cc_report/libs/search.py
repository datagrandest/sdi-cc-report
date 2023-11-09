import re


def get_filter_word(word):
    regex = re.compile(
        "(id|title|content|date|category|favorite|text)? *(%:%|%:|:%|:|<<|<=|>=|><|<|>|=|nn)? *(.*)"
    )
    word_groups = regex.findall(word)
    if word_groups and len(word_groups):
        field = word_groups[0][0].strip() or "text"
        comparator = word_groups[0][1].strip() or ":"
        value = word_groups[0][2].strip() or ""
        no = True if value.startswith("!") else False
    return {
        "word": word,
        "field": field,
        "no": no,
        "comparator": comparator,
        "value": value[1:] if no else value,
    }


def add_exclude_tags(search="", exclude_tags=[]):
    exclude_tags_not = ["!" + tag for tag in exclude_tags]
    search += "+" + "+".join(exclude_tags_not)
    return search


def remove_all_tag(search="", all_tag="@all"):
    search_array = search.split("+")
    search_array.remove(all_tag)
    search = "+".join(search_array) if len(search_array) else ""
    return search


def get_where_array(search=None, all_tag="@all", exclude_tags=[]):
    search = "" if not search or search is None else search

    if all_tag not in search.split("+"):
        search = add_exclude_tags(search, exclude_tags)
    else:
        search = remove_all_tag(search, all_tag)

    where = []
    and_words = [s.strip() for s in search.split("+") if s and s is not None]
    for and_word in and_words:
        or_words = []
        if "|" in and_word:
            or_words = [w.strip() for w in and_word.split("|") if w and w is not None]
            and_word = or_words.pop(0)

        and_w = get_filter_word(and_word)
        and_w["operator"] = "and"
        where.append(and_w)

        for or_word in or_words:
            or_w = get_filter_word(or_word)
            or_w["operator"] = "or"
            where.append(or_w)

    return where


def get_orderby(orderby=None):
    result = []
    if orderby is not None:
        for field in orderby:
            sort = field[0]
            field = field[1:] if sort in ["+", "-"] else field
            order = "DESC" if sort == "-" else "ASC"
        result.append((field, order))
    return result
