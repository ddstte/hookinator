# Hookinator

## Requirements
* Python 3.6+

## Examples
```python
from hookinator import hookable, hook


class BaseUser:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
    ...

# with in-class declaration

@hookable
class User(BaseUser):
    full_name: str
    
    # create post __init__ hook
    @hook(method="__init__", post=True)
    def set_full_name(self, context):
        self.full_name = f'{self.first_name} {self.last_name}'


user = User(first_name="First", last_name="Last")
assert user.full_name == "First Last"


# or ex-class declaration

@hook(method="__init__", post=True)
def post_init_hook(self, context):
    pass

@hook(method="__init__", post=True)
def validate_first_name(context):
    self.first_name = self.first_name.lower()

post_inti_hook.bind(BaseUser)

user = BaseUser(first_name="First", last_name="Last")
assert user.first_name == "first"
```

```python
from hookinator.helpers import hookable
from hookinator.markers import hook


# with in-class declaration
@hookable
class X:
    @hook(method="__init__", pre=True, post=True)
    def foo(self, contex):
        pass

# or ex-class declaration
class Y:
    pass

@hook(method="__init__", post=True)
def post_init_hook(self, context):
    pass

post_inti_hook.bind(Y)

```