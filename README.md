# Hookinator

## Requirements
* Python 3.6+

## Examples
```python
from hookinator import PostHookMarker, HookinatorMixin

# make hook marker
post_init = PostHookMarker("__init__")



class BaseUser:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
    ...

# add HookinatorMixin to User-class 
class User(HookinatorMixin, BaseUser):
    full_name: str
    
    # create post_init hook
    @post_init
    def set_full_name(self, args, kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'


user = User(first_name="First", last_name="Last")
assert user.full_name == "First Last"


# without inheritance
def _validate_first_name(self, args, kwargs):
    self.first_name = self.first_name.lower()

post_init.bind(BaseUser, _validate_first_name)

user = BaseUser(first_name="First", last_name="Last")
assert user.first_name == "first"
```