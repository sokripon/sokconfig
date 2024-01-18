# sokconfig

Just a simple util for my personal use.
This aims to make it easier to load settings.

## Example

```python
import ast

from sokconfig.settings import Settings
from sokconfig.values import IntValue, ListValue


class Config(Settings):
    a = IntValue(5, min_value=0, max_value=10, post_mutator=lambda x: x + 1)
    b = IntValue(2, min_value=0, max_value=10, extra_validator=lambda x: x % 2 == 0, name="TestValueB")
    c = IntValue(None, pre_mutator=int)
    d = ListValue(None, pre_mutator=ast.literal_eval)
    e = ListValue([], element_type=int)


Config.fill_empty_names()

t = {"a": 1, "TestValueB": 4, "c": "3", "d": "[1,2,3]"}
print(Config.get_values())
Config.set_values(t)
Config.e.append(4)
Config.validate_values()
print(Config.get_values())
```

```
{'a': IntValue(value=6, min_value=0, max_value=10), 'b': IntValue(value=2, min_value=0, max_value=10), 'c': IntValue(value=None, min_value=None, max_value=None), 'd': ListValue(value=None), 'e': ListValue(value=[])}
{'a': IntValue(value=2, min_value=0, max_value=10), 'b': IntValue(value=4, min_value=0, max_value=10), 'c': IntValue(value=3, min_value=None, max_value=None), 'd': ListValue(value=[1, 2, 3]), 'e': ListValue(value=[4])}
```