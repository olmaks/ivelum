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
    text = 'The visual description of the colliding files'
    assert ' '.join(replace_content(text)) == 'The visual™ description of the colliding files'
    text = '/ well-spoken /'
    assert ' '.join(replace_content(text)) == '/ well-spoken™ /'


def test_skip_tm():
    patterns = ['"great', "who'll"]
    for pattern in patterns:
        assert ' '.join(replace_content(pattern)) == pattern


def run_tests():
    test_replace_urls()
    test_add_tm()
    test_skip_tm()


run_tests()
