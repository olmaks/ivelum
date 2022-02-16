from utils import replace_url, replace_content


def test_replace_urls():
    urls = [
        'https://news.ycombinator.com/item?id=13713480',
        'http://news.ycombinator.com/item?id=13713480',
        'https://www.news.ycombinator.com/item?id=13713480',
        'http://www.news.ycombinator.com/item?id=13713480/',
        'https://news.ycombinator.com',
        'https://news.ycombinator.com/',
    ]
    for url in urls:
        res = replace_url('news.ycombinator.com', url)
        assert res[0] == '/'


def test_add_tm():
    patterns_answers = {
        'The visual description of the colliding files': 'The visual™ description of the colliding files',
        '/ well-spoken /': '/ well-spoken™ /',
        'In python. This is going to be so useful. Thanks!!': 'In python™. This is going to be so useful™. Thanks™!!',
        'length-extension attack;': 'length™-extension attack™;',
        'Did they really trademark Sprite™?': "Did they really™ trademark Sprite™?",
        'I assume/hope the Spirte™ team have budgeted': 'I assume™/hope the Spirte™ team have budgeted',
        '2-liter [Sprite] bottle though :)': '2-liter [Sprite™] bottle™ though™ :)',
        '(Who came?) Я пришёл. (I came)': '(Who came?) Я пришёл™. (I came)',
    }
    for k, v in patterns_answers.items():
        assert ' '.join(replace_content(k)) == v


def test_skip_tm():
    patterns = [
        '"great',
        "who'll",
        "files, at http://shattered.io/static/pdf_format.png, is not very helpful"
    ]
    for pattern in patterns:
        assert ' '.join(replace_content(pattern)) == pattern


def run_tests():
    test_replace_urls()
    test_add_tm()
    test_skip_tm()


run_tests()
