# Hookinator

## Requirements
* Python 3.6+

## Examples
```python
# make hook markers
pre_save = PreHookMarker("save")

# add HookinatorMixin to User-class 
class User(HookinatorMixin, models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    
    full_name = models.CharField(...)
    
    # create pre_save hook
    @pre_save
    def set_full_name(self, args, kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'

user = User.objects.create(first_name='First', last_name='Last')
assert user.full_name == 'First Last'

```