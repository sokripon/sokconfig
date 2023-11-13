# sokconfig

Just a simple util for my personal use.
This aims to make it easier to load settings.

## Example

```python
from sokconfig.settings import Settings
from sokconfig.values import IntValue


class Config(Settings):
    a = IntValue(5, min_value=0, max_value=10, mutator=lambda x: x + 1)
    b = IntValue(2, min_value=0, max_value=10, extra_validator=lambda x: x % 2 == 0, name="TestValueB")


Config.fill_empty_names()
Config.validate_values()

t = {"a": 1, "TestValueB": 4}
print(Config.get_values())

Config.set_values(t)
print(Config.get_values())
```

```
{'a': IntValue(value=6, min_value=0, max_value=10), 'b': IntValue(value=2, min_value=0, max_value=10)}
{'a': IntValue(value=4, min_value=0, max_value=10), 'b': IntValue(value=4, min_value=0, max_value=10)}
```