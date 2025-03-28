# json_compare

A library to compare any json string/lists/json-like-objects primarily for tests which are using Karate Style Matching rules and templates (https://github.com/karatelabs/karate?tab=readme-ov-file#fuzzy-matching)

Version 1.0: First version.

## Features

* Compare jsons (recursion supported). Useful for interface testing.
* Compare lists out of order. In order compare is not supported yet.
* Supports Python >=3.5.
* Supports skipping of optional keys using ##object in the expected/template JSON
* Checks if input is valid JSON object before starting the comparison


## QuickStart

install

```shell
pip install jsoncomparekarate
```

or update

```shell
pip install -U jsoncomparekarate
```

a simple example

```python
from jsoncomparekarate import compare
print(compare({"key1":["v1","v2"],"key2":{"key3":1}},{"key1":["v2","v1"],"key2":{"key3":2}}))
```

to see

```
a is {'key1': ['v1', 'v2'], 'key2': {'key3': 1}}
b is {'key1': ['v2', 'v1'], 'key2': {'key3': 2}}

False
```

For more demos and information, just install it and visit the test file **test_json_compare.py** in **Your_Python_Path/Lib/site-packages/json_compare_karate/**

## Bug report

* Issues and bugs report to eatfrogfirst@outlook.com.
* Homepage icon leads to my Github project page, issues / PRs / stars are welcomed :)
