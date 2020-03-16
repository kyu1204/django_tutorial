# First django project
> RESTful API 

## django-restful-swagger bug fix
1. restful-swagger settings change (OpenApi -> CoreApi)
>venv/Lib/site-packages/rest_framework/settings.py
>
>'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema', -> 
>'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema', 

2. load 'staticfiles' bug fix 
>venv/Lib/site-packages/rest_framework_swagger/templates/rest_framework_swagger/index.html
>
>{% load staticfiles %} -> {% load static %}