#!/usr/bin/env python
# coding: utf-8
from jsoncomparekarate import compare

def long_line():
    print("-" * 120)


def run_tests():
    #keys must be str, int, float, bool or None, not bytes
    # a = {"姓名": "王大锤"}  # str and unicode (or bytes and str in python3) are compatible, useful in Chinese words...
    # b = {"姓名".encode("utf-8"): "王大锤".encode("utf-8")}
    # assert compare(a, b)
    # long_line()

    a = [[1, 2, 3], [4, 5, 6]]  # tuples and lists cannot be compared
    b = ([6, 5, 4], [3, 2, 1])
    assert not compare(a, b)
    long_line()

    a = [[1, 2, 3], [4, 5, 6]] # by default order is ignored, so these two are same
    b = [[3, 2, 1], [6, 5, 4]]
    assert compare(a, b)
    long_line()

    a = {"a": 1, "b": 3, "c": False, "d": "ok"}
    b = {"a": 1, "b": 2, "c": "False", "e": "ok"}  # False != "False"
    assert not compare(a, b)
    long_line()

    a = {"a": [1, {"k": ["ok"]}]}
    b = {"a": [1, {"k": ["error"]}]}  # ignoring list order, we aren't sure to pair {"k": ["ok"]} with {"k": ["error"]}
    assert not compare(a, b)
    long_line()

    a = {"a": [1, {"k": [0]}]}  # ignore path ["/a/1/k"] by specifying it as a list in the template
    b = {"a": [1, {"k": "#list"}]}
    assert compare(a, b)
    long_line()

    # a = [{"a": 1, "b": 2}, {"a": 5, "b": 4}]  # now we finally support regular expressions in ignore_path list
    # b = [{"a": 3, "b": 2}, {"a": 6, "b": 4}]  # in this case, only value of "b" concerned
    # check(a, b, ignore_list_seq=False, ignore_path=[r"^(/\d+/a)"])
    # long_line()

    # a = [{"a": 1, "b": 2}, {"a": 1, "b": 4}]  # also useful under list_seq ignored
    # b = [{"a": 2, "b": 4}, {"a": 2, "b": 2}]
    # check(a, b, ignore_path=[r"^(/\d+/a)"])
    # long_line()

    # a = [{"a": 1, "b": 3}, {"a": 1, "b": 4}]  # this time, 3 and 2 cannot match
    # b = [{"a": 2, "b": 4}, {"a": 2, "b": 2}]
    # assert not compare(a, b, ignore_path=[r"^(/\d+/a)"])
    # long_line()

    # a = [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 4}]  # this time, only different frequency found
    # b = [{"a": 6, "b": 4}, {"a": 7, "b": 2}, {"a": 8, "b": 2}]  # but it will choose a random value of "a" to display
    # assert not compare(a, b, ignore_path=[r"^(/\d+/a)"]) # it's caused by logic restriction, don't get confused
    # long_line()

    a = {"a": [1, {"k": "#[_>0]", "l": "#bool"}, 3]}  # ignore two paths this time, "/a/1/k" and "/a/1/l"
    b = {"a": [1, {"k": [1], "l": False}, 3]}
    assert compare(a, b)
    long_line()

    a = '{"rtn": 0, "msg": "ok"}'  # can compare json string with python dict/list objects
    b = {"rtn": 1, "msg": "username not exist"}
    assert not compare(a, b)
    long_line()

    a = u'{"body":{"text":"你好"}}'  # both text and binary json strings are supported
    b = '{"body":{"text":"你好啊"}}'
    assert not compare(a, b)
    long_line()

    a = [1, 2, 2]  # even we ignore the order, the frequency of elements are concerned
    b = [1, 1, 2]
    assert not compare(a, b)
    long_line()

    a = [1, 2, 3]
    b = [1, 3, 4, 5]  # even if the length of lists are not equal, we can still know the difference
    assert not compare(a, b)
    long_line()

    a = [1, 2, 3]
    b = [1, 3, 4, 5]  # but we CANNOT keep the order of elements under different length even if ignore_list_seq is False
    assert not compare(a, b)
    long_line()

    a = [1.0]  # in face cp.compare(1, 1.0) is allowed, however non-standard jsons are not recommend
    b = [1]  # Integers and floats are compatible, including long of python 2
    assert compare(a, b)
    long_line()

    a = ["#regex ^(.*)$"]  # re-comparing enabled as default. Be careful bare r"^(.*)$" without list is considered as json-str
    b = ["anything"]  # use this to skip any unconcerned fields
    assert compare(a, b)
    long_line()

    a = ["#regex (.*)"]  # without ^-start or $-end, this won't be regarded as re-pattern
    b = ["anything"]
    assert compare(a, b)
    long_line()

    a = ["#regex ^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$"]  # we can use re-comparing to confine formats but not values
    b = ["anything"]
    assert not compare(a, b)
    long_line()

    a = ["#regex ^(2019-07-01 \d{2}:\d{2}:\d{2})$"]  # e.g. this assertion will pass
    b = ["2019-07-01 12:13:14"]
    assert compare(a, b)
    long_line()

    a = ["#regex ^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$", "#regex ^(.*)$"]
    b = ["anything", "otherthing"]  # when using re with order-ignored list, it will be crossing compare
    # be careful, potential chance of messy
    assert not compare(a, b)
    long_line()

    a = ["#regex ^(.*)$"]  # two re-pattern is not allowed
    b = ["#regex ^(.+)$"]
    try:
        compare(a, b)
    except Exception as e:
        print(e)
    else:
        raise AssertionError()
    long_line()

    a = ["#regex ^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})$", "otherthing"]
    b = ["anything", "#regex ^(.*)$"]  # this errors when comparing a[0] with b[1] due to the above rule
    try:
        compare(a, b)
    except Exception as e:
        print(e)
    else:
        raise AssertionError()
    long_line()

    a = '["^(2019-07-01 \\d{2}:\\d{2}:\\d{2})$"]'  # cannot compare a string and a list
    # or use '["^(2019-07-01 \\\\\d{2}:\\\\\d{2}:\\\\\d{2})$"]' will also work
    b = ["2019-07-01 12:13:14"]
    assert not compare(a, b)
    long_line()

    a = r'[r"^(2019-07-01 \d{2}:\d{2}:\d{2})$"]'  # cannot compare a string and a list
    b = ["2019-07-01 12:13:14"]
    assert not compare(a, b)
    long_line()

    a = ["#regex ^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"]  # only fully match will pass re-comparing
    b = ["2019-07-01 12:13:14.567"]
    assert compare(a, b)
    long_line()

    a = ["#regex ^.*?(\d)-(\d)"]  # matching regex
    b = ["2019-07-01 12:13:14.567"]
    assert compare(a, b)
    long_line()

    a = [0.1 + 0.1 + 0.1]  # default we use accurate compare, since float compute causes accumulative errors
    b = [0.3]
    assert not compare(a, b)
    long_line()

    #check(a, b, ignore_list_seq=False, float_fuzzy_digits=6)  # so we can bear margin < 10e-6 now in float comparing
    # long_line()

    a = {"key": 1}
    b = {"key": 1.0}
    assert compare(a, b)
    long_line()

    #assert not compare(a, b)
    # long_line()

    a = {"a": {"b": 1, "c": 2, "d": 3}} # skip comparing "/a/b" and "/a/d"
    b = {"a": {"b": "##object", "c": 2, "d": "##object"}}
    assert compare(a, b)
    long_line()

    a = {"a": {"b": 1, "c": 2}}
    b = {"a": {"b": "##object", "c": 2, "d": 3}}
    # assert not compare(a, b, omit_path=["/a/b"])
    assert not compare(a, b)
    long_line()

    a = {"a": [{"b": 1, "c": 2}, {"d": 3, "c": 4}]} # omit paths "a/b" and "a/d"
    b = {"a": [{"b": "##object", "c": 2}, {"c": 4, "d": "##object"}]}
    assert compare(a, b)
    long_line()

    a = {"a": [{"b": 1, "c": 2}, {"c": 2}, {"d": 3, "c": 4}]}
    b = {"a": [{"b": "##object", "c": 2}, {"c": 4}, {"c": 4, "d": "##object"}]}
    assert not compare(a, b)
    long_line()

    a = { "data": "#regex unified-text:text-flow:text-max-chars.+" }
    b = { "data": "unified-text:text-flow:text-max-chars.plus-extra-chars" }
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#string"}
    b = {"data": "some-random-string"}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#number"}
    b = {"data": 100}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#object"}
    b = {"data": { "key1" : "value1", "key2" : "value2" }}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#list"}
    b = {"data": ["item1", "item2"]}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#[]"}
    b = {"data": ["item1", "item2"]}
    assert not compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#[]"}
    b = {"data": []}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#[_ > 0]"}
    b = {"data": ["item1", "item2"]}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#[_ > 0]"}
    b = {"data": []}
    assert not compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#[_ >= 0]"}
    b = {"data": []}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {"data": "#[]"}
    b = {"data": []}
    assert compare(a, b)  # two strings with regular expression
    long_line()

    a = {
       "id": "file",
       "value": "File",
       "popup": {
          "menuitem": [
             {"valueld1": "New", "onclickld1": "CreateNewDoc()"},
             {"valueld2": "Open"},
             {"valueld3": "Close", "onclickld3": "CloseDoc()"}
          ],
          "optionalItem": {}
       }
    }
    b = {
       "id": "#string",
       "value": "##string",
       "popup": {
          "menuitem": [
              {"valueld3": "Close", "onclickld3": "CloseDoc()"},
              {"valueld2": "Open", "onclickld2": "##string"},
              {"valueld1": "New", "onclickld1": "CreateNewDoc()"}
          ],
          "optionalItem": "#object",
          "notNeededItem": "##object"
       }
    }
    assert compare(a, b, strict_json_check = True)
    long_line()

    # add support for optional fields for these tests
    # a = {}
    # b = {'a': '##null'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {}
    # b = {'a': '##notnull'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {}
    # b = {'a': '#notpresent'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {}
    # b = {'a': '#ignore'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': None}
    # b = {'a': '#null'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': None}
    # b = {'a': '##null'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': None}
    # b = {'a': '#present'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': None}
    # b = {'a': '#ignore'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': 1}
    # b = {'a': '#notnull'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': 1}
    # b = {'a': '##notnull'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': 1}
    # b = {'a': '#present'}
    # assert compare(a, b)
    # long_line()
    #
    # a = {'a': 1}
    # b = {'a': '#ignore'}
    # assert compare(a, b)
    # long_line()


if __name__ == "__main__":
    run_tests()
