<div align="center">
    <h1> Testing </h1>
</div>

## Test structure

Test cases will typically have a format such as this,

```python
class YourTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass
    
    @classmethod
    def setUpTestData(cls):
        # Will be only ran once, to create reusable test data.
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)
```

## Running all tests

To execute all tests, the following command can be used.

```commandline
python manage.py test
```

This will discover all files named with the pattern test*.py under the current directory and run all tests defined 
using appropriate base classes.

If your tests are independent, on a multiprocessor machine you can significantly speed them up by running them in 
parallel. The use of --parallel auto below runs one test process per available core. The auto is optional, and you can 
also specify a particular number of cores to use.

## Speeding up test execution time.

```commandline
python manage.py test --parallel auto
```

## Running an individual test

If you want to run a subset of your tests you can do so by specifying the full dot path to the package(s), module,
`TestCase` subclass or method, e.g.

```commandline
# Run all tests inside the tests file 
python manage.py test weighttracking.tests.test_models

# Run all tests for the given class
python manage.py test weighttracking.tests.test_models.WeightTrackingModelTest

# Run a specific test inside the class
python manage.py test weighttracking.tests.test_models.WeightTrackingModelTest.test_weight_tracking_model_creation
```

## Test structure

The generated app will provide a `tests.py`, however, I much prefer to change the structure to the following,

```commandline
app_example/
  /tests/
    __init__.py
    test_models.py
    test_views.py
```

In order to not bloat the single file with every test type.