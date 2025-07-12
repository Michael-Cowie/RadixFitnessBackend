<div align="center">
    <h1> Code Style - Source Code </h1>
</div>

Black and isort are Python formatting tools that will are ran over the repository. Once a pull request has been made the GitHub Action workflow will run to make sure the code is an acceptable format before it can be merged. Any subsequent commits will also rerun the tests.

Due to the repository size, it's completely acceptable to resolve any formatting problems by running the scripts to 
format the code over the entire repository. 

To resolve all formatting issues, simply run `format_code.cmd` within the `app` directory.

<div align="center">
    <h1> Code Style - Handling Requests </h1>
</div>


In Django REST Framework, views are responsible for

1. Receiving and parsing HTTP requests
2. Validating and parsing HTTP requests
3. Executing business
4. Returning well-structured responses


To accomplish this, DRF provides a robust **serializer system** and class-based view architecture. The key terminology to understand
in this area are

- **Serializer** - A component in DRF that **acts like a translator** between complex Python objects such as Django models and primitive data types, commonly JSON. It also performs **input validation**
- **Deserialization** - The process of converting incoming raw data, typically received in formats such as JSON, XML, or form data, into native Python data types that can be easily manipulated within the Django application. 
- **Schema** - A definition of expected data structure. For example, JSON Schema defines what valid JSON looks like.

## Validation Before Processing

Validation is the process of ensuring that input data adheres to expected formats and constraints before acting on it. In DRF, **serializers are the primary validation mechanism**. Manually validating `request.data` should be avoided in favour of declarative, reusable serializer logic.

**Avoid**

```python
name = request.data.get("name")
if not name:
    return Response({"error": "Missing name"}, status=400)
```

**Prefer**

```python
serializer = ExampleSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
```

In DRF, serializers are essential for parsing, validating and transforming incoming request data and formatting outgoing responses. Two primary serializer types exists.

- **ModelSerializer** - Tightly coupled to Django models, automating many common CRUD operations.
- **Serializer** - A flexible defined serializer for arbitrary data validation and transformation.

Data can be passed into serializers in two ways, `instance` and `data`.

Use `instance=...` when you want to turn Python objects (like model instances or dicts) into JSON-friendly data. When you see `instance`, think "I am reading and serializing this object".

```python
user = User.objects.get(id=1)
serializer = UserSerializer(instance=user)
```

Use `data=...` when you want to accept input (usually from a request) and validate it before saving or processing it. This is what you will do in `POST`, `PUT` or `PATCH` operations. When passing data through with `data=...` you must also call `is_valid()`.

```python
data = {"username": "johndoe", "email": "john@example.com"}
serializer = UserSerializer(data=data)
serializer.is_valid(raise_exception=True)
user = serializer.save()
```

## Serializer Inputs

DRF serializers accept two primary parameters that determine their operational mode,

1. `instance` - Converts model instances to JSON (Serialization).
2. `data` - Validates incoming JSON data (Deserialization).
3. **Both** - Updates existing instances with new data.

#### Instance Parameter

The purpose of inputting only the `instance` parameter is to perform the conversion **from a Django model instance to a JSON representation** for API responses.

This will be primarily used for GET endpoints, response formatting and data transformation. This type of transformation is read-only, performs **no validation** and accessed via `serializer.data`.

```python
# Single instance
user = User.objects.get(id=1)
serializer = UserSerializer(user)
json_output = serializer.data

# Multiple instances
users = User.objects.all()
serializer = UserSerializer(users, many=True)
json_output = serializer.data
```

#### Data Parameter

The purpose of inputting only `data` into a serializer **is to perform the conversion of JSON data into a Django model instance**. This will perform model validation and processing.

This is primarily used for POST endpoints. It will perform **input validation** and resource creation. You must call `is_valid()` and access the data via `serializer.validated_data`. 

There are multiple patterns for passing the `data` pattern such as,

1. **Validation and Automatic Save**

```python
serializer = UserSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
user = serializer.save()
```

2. **Validation and Manual Processing**

```python
serializer = UserSerializer(data=request.data)
serializer.is_valid(raise_exception=True)

user, created = User.objects.update_or_create(
    email=serializer.validated_data['email'],
    defaults=serializer.validated_data
)
```

The `update_or_create()` treats every positional/keyword argument **except** `defaults` as part of the look up that decides whether a row already exists.

In the following example we want to search for the user `request.user`, which is the primary key and then create or update
the columns specified under `defaults`. Any fields in `defaults` are applied as an atomic `UPDATE` if the row exists or used to populate a new row if it doesn't.

```python
instance, created = Profile.objects.update_or_create(
    user=request.user,                       #  <-- lookup key(s)
    defaults={
        "name": serializer.validated_data["name"],
        "measurement_system": serializer.validated_data["measurement_system"],
    },                                       #  <-- fields to update / set
)
```

This is generally shortened to pass `serializer.validated_data` using the request serializer, demonstrated previously with `UserSerializer`.

#### Combined Usage

The purpose of passing both an instance with data, is to **update existing instances with validated data**. This will primarily to be used for PUT/PATCH for resource updating. For `patch`, you would need to pass `partial=True` to the serializer.

```python
user = User.objects.get(id=1)
serializer = UserSerializer(user, data=request.data)
if serializer.is_valid():
    updated_user = serializer.save()
```

## Model Serializers

`ModelSerializer` is a subclass of `Serializer` that automatically generates fields from a Django model. It simplifies the creation
of serializers for **typical CRUD operations**. Use `ModelSerializer` when the incoming or outgoing data **directly represents a database model instance or queryset**. It is ideal for operations that create, retrieve, update, or delete model-backed resources.

The `ModelSerializer` also implements default `create()` and `update()` methods as well as supporting `.save()` **to persist instances to the database**. The field instances are inferred from the model, unlike a `Serializer`. Additionally, field model validation is automatic, unlike `Serializer`.

| HTTP Method | Use Case for ModelSerializer                                  | Example Scenario                         |
| ----------- | ------------------------------------------------------------- | ---------------------------------------- |
| **GET**     | Serialize model instances or collections for read operations. | Returning a list of `Article` records.   |
| **POST**    | Create a new model instance with validated data.              | Creating a new `Order` record.           |
| **PUT**     | Fully update or replace a model instance.                     | Replacing all fields of a `UserProfile`. |
| **PATCH**   | Partially update specific fields on a model instance.         | Updating a user's email or address only. |
| **DELETE**  | Typically no serializer needed; deletion is by identifier.    | Deleting a specific `Comment` by ID.     |

Use the naming convention `<ModelName><Purpose>Serializer`

| Use Case            | Example Serializer Name         | HTTP Method | Description                              |
|---------------------|--------------------------------|-------------|------------------------------------------|
| Retrieve - GET      | `BookDetailSerializer`          | GET - Detail | Detailed view of a single object         |
| List - GET          | `BookListSerializer`            | GET - List  | Summary view for multiple objects        |
| Create - POST       | `BookCreateSerializer`          | POST        | Used to create new instances              |
| Update - PUT/PATCH  | `BookUpdateSerializer`          | PUT, PATCH  | Update existing objects                    |
| Create or Update    | `BookUpsertSerializer`          | PUT         | For `update_or_create` semantics          |
| Partial Update      | `BookPartialUpdateSerializer`   | PATCH       | Partial updates, fewer required fields    |

### ModelSerializer Database Level Validation

While `ModelSerializer` automatically performs field-level validation (e.g. required fields, max length and types), however it **does not automatically validate model-level constraints** such as,

- `unique_together`
- `UniqueConstraint`
- ...

These constraints are enforced **only at the database level**, meaning `serializer.is_valid()` will **still pass** even if the input would violate them. This can result in `IntegrityError` when `serializer.save()` is called. **You must manually validate these constraints at the serializer level**.

**Definition**

This model ensures that each user can only have one weight entry per day, **enforced at the database level**.

```python
class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight_kg = models.FloatField(validators=[MinValueValidator(1)])
    notes = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ("date", "user")
```

**Serializer Definition**

```python
class WeightEntryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ("date", "weight_kg", "notes")

    def create(self, validated_data):
        return WeightEntry.objects.create(user=self.context["user"], **validated_data)
```

This serializer **does not check for duplicates**. A second POST with the same `user` and `date` would pass `.is_valid()` but crash on `.save()` with a `django.db.IntegrityError`. To implement the correct serializer of this, we need to add manual uniqueness validation.

```python
class WeightEntryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightEntry
        fields = ("date", "weight_kg", "notes")

    def validate(self, attrs):
        user = self.context["user"]
        date = attrs["date"]

        if WeightEntry.objects.filter(user=user, date=date).exists():
            raise serializers.ValidationError("You already have a weight entry for this date.")

        return attrs

    def create(self, validated_data):
        return WeightEntry.objects.create(user=self.context["user"], **validated_data)
```

### Response ModelSerializer

Response serializers are used to format model data for output, commonly in GET requests. When building response-only serializers, we need to maintain a balance of maintainability and safety.

When using a `Serializer` with manually declared fields this leads to duplication,

- Requires replicating model field types, constraints and naming.
- Becomes difficult to keep in sync with model changes.
- Introduces risk of stale or incorrect representations.

Using `ModelSerializer` auto-generates fields from the model, keeping serializers synchronized.

- Reduces boilerplate.
- Tracks model changes automatically.
- Preferred for large or evolving schemas.

`ModelSerializer` also enables write access by default. If a response serializer is mistakenly used in a POST or PUT it may modify sensitive fields. Therefore, it's essential mark all fields as read only.

```python
class ProfileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'bio', 'created_at']
        read_only_fields = fields
```

This will prevent accidental misuse for a response based serializer from accidentally changing data in the model.

When you declare fields as `read_only_fields`, those fields are not allowed in `input` data. Meaning,

- The serializer ignores them during `is_valid()`
- They are excluded them validation
- They are not included in `.invalidated_data`

They are still included in the output via `.data`, but RDF treats them if they don't exist for writes such as `create()` or `update()` calls. This makes it a perfect use for response serializers.

### ModelSerializer - GET

The `GET` method is used to **retrieve data**, typically for,

- Listing records, such as a `GET /resources/`.
- Viewing a single resource, such as `GET /resources/<id`

Use `ModelSerializer` when returning **model instances** or **querysets**. It automatically handles the conversion of Django ORM objects to native Python data types and finally JSON.

**Definition**
```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
```

**Usage**
```python
def get(self, request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
```

### ModelSerializer - POST

The `POST` method is used to **create new resources** or **trigger actions**.

Use `ModelSerializer` when creating a new instance of a model from validated data.

**Definition**
```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "price"]
```

**Usage**
```python
def post(self, request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save()
    return Response(ProductSerializer(product).data, status=201)
```

### ModelSerializer - PUT

The `PUT` method is meant for a complete replacement of a resource. It is also commonly used for idempotent upserts, where

- If the resource exists → it is updated.
- If it does not exist → it is created.

This requires the use of `get_or_create()` or `update_or_create()` patterns in Django.

Use `ModelSerializer` when the input data is mapped directly to a model and the behaviour should be

- Replace all relevant of the object exists.
- Create the object if it doesn't.

**Definition**
```python
class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField()

    class Meta:
        unique_together = ("user", "date")
```

Each user can only have one `DailyLog` per day.

**Serializer**

`DailyLogSerializer` is a `ModelSerializer` used to create or update `DailyLog` entries associated with a specific user and date. It encapsulates the logic for conditionally or updating a record, based on the uniqueness constraint defined in the `DailyLog` model.

The Django model constraint,

```python
class Meta:
    unique_together = ("user", "date")
```

only enforces uniqueness at the **database level**, they do not prevent a serializer attempting to create duplicate entries. Without custom logic in the serializer, using `is_valid()` followed by `.save()` could cause a `django.db.IntegrityError` if a duplicate `DailyLog` already exists.

To prevent this, we override the `create()` method to ensure that either a new entry is created or an existing entry is updated - **without violating model constraints**.

The `create(self, validated_data)` is invoked when `.save()` is called on the serializer. It is **not bound to an instance**.

The `update(self, instance, validated_data)` is invoked when `.save()` is called on a serializer **bound to an existing instance**. 

`update()` will be primarily called using `PUT` and `PATCH` whereas `create()` will be primarily used for `POST`.

```python
from rest_framework import serializers
from .models import DailyLog

class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        fields = ["notes"]  # only include mutable fields

    def create(self, validated_data):
        user = self.context["user"]
        date = self.context["date"]

        instance, _ = DailyLog.objects.update_or_create(
            user=user,
            date=date,
            defaults=validated_data,
        )
        return instance

    def update(self, instance, validated_data):
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()
        return instance

class DailyLogQuerySerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
```

`user` and `date` are passed via `context` and **not exposed to the client**. This avoids them being tampered with.

**Usage**
```python
def put(self, request):
    query_serializer = DailyLogQuerySerializer(data=request.query_params)
    query_serializer.is_valid(raise_exception=True)

    body_serializer = DailyLogSerializer(
        data=request.data,
        context={"user": request.user, "date": query_serializer.validated_data["date"]},
    )
    body_serializer.is_valid(raise_exception=True)
    instance = body_serializer.save()

    return Response(DailyLogSerializer(instance).data, status=200)
```

### ModelSerializer - PATCH

The `PATCH` method is used for **partial updates** to a resource.

You should use the `ModelSerialzer` when updating only some fields of a model.

**Definition**
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
```

**Usage**
```python
def patch(self, request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(instance=user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()  # partial update
    return Response(serializer.data)
```

### ModelSerializer - DELETE

The `DELETE` method is used to **remove a resource**. Usually, no serializer is needed.

In most cases, no serializer is required for deltes. You simply act on a model isntance.

```python
def delete(self, request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return Response(status=204)
```

## Non-Model Serializers.

`Serializer` is a manually defined serializer class for validating and transforming arbitrary input or output data **that is not tied to a Django model**. You must define all fields, validation rules and persistence logic manually.

- **Validating non-model data**, e.g. login credentials and filter parameters
- Returning computed or aggregated values.
- Processing multi-object payloads or inputs to business logic.
- Serializing read-only structures, e.g. reports and summaries

When using a `Serializer`, each input is not tied to a model and thus each field must be defined manually. This is primary used for input validation
that **will not serialize to a model**.

When using a Serializer,

- If you're passing `data=...` call `is_valid()`. You want to use `data=` if you want to validate arbitrary raw input.
- If you're passing `instance=...`, you're just serializing and `is_valid()` is not needed.

Use the naming convention `<Purpose>Serializer`

| Purpose           | Name                             |
| ----------------- | -------------------------------- |
| Custom input only | `PasswordResetRequestSerializer` |
| Query param       | `ReportQuerySerializer`          |
| Output only       | `HealthCheckResponseSerializer`  |
| Mixed fields      | `DateRangeFilterSerializer`      |

### Serializer - GET

Use `Serializer` when returning **computed, external**, or **non-model data**.

Let's say we generate a `DailyReport` in memory, so that it's not stored in a model. We want to,

1. Construct the report in view logic.
2. Validate it using DRF serializer logic.
3. Return the cleaned result in the response.

**Definition**
```python
from rest_framework import serializers

class DailyReportSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_tasks = serializers.IntegerField(min_value=0)
    completed_tasks = serializers.IntegerField(min_value=0)

    def validate(self, data):
        if data["completed_tasks"] > data["total_tasks"]:
            raise serializers.ValidationError("Completed tasks cannot exceed total tasks.")
        return data
```

**Usage**
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date

class DailyReportView(APIView):
    def get(self, request):
        # Raw, unvalidated internal data.
        raw_report = {
            "date": date.today(),
            "total_tasks": 10,
            "completed_tasks": 5,
        }

        serializer = DailyReportSerializer(data=raw_report)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
```

### Serializer - POST

The `POST` method is used to **create new resources** or **trigger actions**.

Use `Serializer` when the `POST` is not about saving to a model but rather,

- Authenticating users.
- Sending an email.
- Validating structured input.

**Definition**
```python
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
```

**Usage**
```python
def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    return Response({"token": make_token(user)})
```

### Serializer - PUT

The `PUT` method is used to fully replace an existing resource.

Use `Serializer` when you want to process full replacement of **structured data not stored in a model**.

**Definition**
```python
class SystemConfigSerializer(serializers.Serializer):
    timezone = serializers.CharField()
    email_notifications = serializers.BooleanField()
```

**Usage**
```python
def put(self, request):
    serializer = SystemConfigSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    update_external_config(serializer.validated_data)
    return Response({"status": "updated"})
```

### Serializer - PATCH

The `PATCH` method is used for partial updates to a resource.

Use `Serializer` when updating **external configurations, stateful settings** or **non-model representations**.

**Definition**
```python
class NotificationSettingsSerializer(serializers.Serializer):
    email = serializers.BooleanField(required=False)
    sms = serializers.BooleanField(required=False)
```

**Usage**
```python
def patch(self, request):
    serializer = NotificationSettingsSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    apply_notification_settings(serializer.validated_data)
    return Response({"status": "settings updated"})
```

### Serializer - DELETE

The `DELETE` method is used to **remove a resource**. Usually, no serializer is needed.

Use `Serializer` if,

- You need to accept additional parameters for conditional deletions.
- You require pre-validation before deletion.

**Definition**
```python
class DeletionRequestSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False)
```

**Usage**
```python
def delete(self, request):
    serializer = DeletionRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    log_deletion_reason(serializer.validated_data.get("reason"))
    delete_something()
    return Response(status=204)
```