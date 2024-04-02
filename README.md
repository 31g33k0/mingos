# Mingos Project

This is a learning project to understand how to use the Django framework. The project is a simple web application that allows users to create, read, update, and delete (CRUD) resources. The project is called Mingos as a homage to Charles Mingus, the jazz musician.

## Getting Started
First, we initialized a virtual environment:

```bash
python3 -m venv venv
```

Then, we activated the virtual environment:

```bash
source venv/bin/activate
```

now we are ready to install the dependencies:

```bash
pip install django djangorestframework
```

Now we can freeze the dependencies:

```bash
pip freeze > requirements.txt
```

### Starting a Django Project
To start a Django project, we run the following command:

```bash
django-admin startproject mingos .
```

This will initialize a Django project in the _current directory_.

### Adding a Django App
To add a Django app, we run the following command:

```bash
python3 manage.py startapp api
```

This will create a Django app called `api`. (We can also create the app by hand, by creating a directory with a `__init__.py` file and a `models.py` file.)

### Registering the Django App
We added the App, but django does not know about it yet.
In order to use urls, models, templates, etc. from the app, we need to register the app with the Django project.

To register the Django app, we add the app to the `INSTALLED_APPS` list in the [`mingos/settings.py`](mingos/settings.py) file:

```python
INSTALLED_APPS = [
    #...

    'rest_framework',

    'api',
]
```

### Testing if everything is working
To test if everything is working, we can run the following command:

```bash
python3 manage.py runserver
# the website is available on http://localhost:8000
```


### Models
Models are the data that our application will work with. We define models in the `models.py` file inside of the app directories.

For example we want to create a model for `Sleep`:

```python
from django.db import models

from datetime import datetime

class Sleep(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    hours = models.FloatField(null=False, blank=False)
    quality = models.IntegerField(default=5)
    notes = models.TextField(null=False, blank=True)

    # This is the readable representation of the model, otherwise
    # it would just be displayed as 'Sleep object(1)'
    def __str__(self):
        return f'{self.date} - {self.hours} hours'
```

### Migrations
After we define the models, we need to create the database tables that will store the data. We do this by running the following command:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Admin Interface
Django provides an admin interface that allows us to interact with the data in the database. To use the admin interface, we need to create a superuser:

```bash
python3 manage.py createsuperuser
# Username (leave blank to use 'user'): chronominet
# Email address: admin@example.com
# Password: vivelabiere
# Password (again): vivelabiere
```

Then we can run the server and navigate to the admin interface:

```bash
python3 manage.py runserver
# the admin interface is available on http://localhost:8000/admin
```
### Registering our model with the admin interface

To register our model with the admin interface, we need to create (or edit) the `admin.py` file in the api app directory:

```python
from django.contrib import admin
from .models import Sleep

admin.site.register(Sleep)
```

now we can see and manage the `Sleep` model in the admin interface.


### Modifying the Model
We want to modify the model to add a `owner` field that will link the sleep to the user that created it. We will use a ForeignKey to do this.

```diff
  from django.db import models
+ from django.contrib.auth.models import User
  
  from datetime import datetime
  
  class Sleep(models.Model):
      date = models.DateTimeField(default=datetime.now, blank=True)
      hours = models.FloatField(null=False, blank=False)
      quality = models.IntegerField(default=5)
      notes = models.TextField(null=False, blank=True)
+     owner = models.ForeignKey(
+         User, on_delete=models.CASCADE, null=False, blank=False
+     )
```

Since we changed the model, it will also need to be modified in the database. We can create a migration to do that, and apply it.

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

This will cause some problems, since we have existing data in the database that does not have an owner. We provide a one-off default value for the owner field by selecting option 1, and providing the id of the user that we want to be the owner of the existing data. ("1" for the admin.)

## Creating a REST API
Regular users cannot interact with the data using the admin interface, so we want to create a REST API that will allow users to query and modify the data.

### Serializers
Serializers are used to convert Django models to JSON, and vice versa.
We want to define a serializer for the `Sleep` model in the [`serializers.py`](api/serializers.py) file:

```python
from rest_framework import serializers

from .models import Sleep

class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        # The required fields are the model, and the fields that will be
        # displayed back to the user.
        model = Sleep
        fields = ['id', 'date', 'hours', 'quality', 'notes', 'owner']

```

### Views
Views are used to define the behavior of the API. We want to define a view for the `Sleep` model in the [`views.py`](api/views.py) file:

```python
from rest_framework import generics
from .models import Sleep
from .serializers import SleepSerializer

class SleepList(generics.ListCreateAPIView):
    queryset = Sleep.objects.all()  # get all objects from database
    serializer_class = SleepSerializer

```

### URLs
Now we need to define _where_ the API endpoint will be available. We do this by defining the URL in the [`urls.py`](api/urls.py) file:

```python
# api/urls.py
from django.urls import path
from .views import SleepList

urlpatterns = [
    path('sleep/', SleepList.as_view(), name='sleep-list'),
]
```

and we need to include our app urls in the main project urls in the [`mingos/urls.py`](mingos/urls.py) file:

```diff
# mingos/urls.py
- from django.urls import path
+ from django.urls import include, path

  # ...
  
  urlpatterns = [
      path('admin/', admin.site.urls),
+     path('api/', include('api.urls')),
  ]
```
(if this does not work, make sure that the api app is registered in the `INSTALLED_APPS` list in the [`mingos/settings.py`](mingos/settings.py) file.)

### Testing the API
We can now navigate to [http://localhost:8000/api/sleep/](http://localhost:8000/api/sleep/) to see the API endpoint.

### Adding Authentication
We want to add authentication to the API, so that only authenticated users can interact with the data.

We can do this by adding the `permission_classes` attribute to the view:

```diff
  from rest_framework import generics
+ from rest_framework.permissions import IsAuthenticated
  from .models import Sleep
  
  from .serializers import SleepSerializer
  
  class SleepList(generics.ListCreateAPIView):
      queryset = Sleep.objects.all()
      serializer_class = SleepSerializer
+     # only authenticated users can view and create data
+     permission_classes = [IsAuthenticated]
```

We also want to automatically set the owner of the data to the current user:

```diff
  from rest_framework import generics
  from rest_framework.permissions import IsAuthenticated
  from .models import Sleep
  
  from .serializers import SleepSerializer
  
  class SleepList(generics.ListCreateAPIView):
      queryset = Sleep.objects.all()
      serializer_class = SleepSerializer
      # only authenticated users can view and create data
      permission_classes = [IsAuthenticated]

+     def perform_create(self, serializer):
+       # set the owner of the sleep to the current user
+       serializer.save(owner=self.request.user)
```

We can also add a second serializer for creating Sleep objects:

```python
class CreateSleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        # We do not want to let the user control the owner field.
        fields = ['date', 'hours', 'quality', 'notes']
```

and then we can switch between the serializers in the view:

```diff
- from .serializers import SleepSerializer
+ from .serializers import SleepSerializer, CreateSleepSerializer

  class SleepList(generics.ListCreateAPIView):
      queryset = Sleep.objects.all()
-     serializer_class = SleepSerializer
      permission_classes = [IsAuthenticated]

+     def get_serializer_class(self):
+         if self.request.method == 'GET':
+             return SleepSerializer
+         return CreateSleepSerializer
```