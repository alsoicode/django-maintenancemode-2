# django-maintenancemode-2

Current Version: 1.1.0

This project makes it easy to put your Django site into "maintenance mode", or more technically, return an HTTP 503 response.

This project differs slightly from other implementations in that the maintenance mode flag is stored in your database versus settings or an environment variable. If your site is deployed to multiple servers, the centralized database-based maintenance flag makes it a snap to bring them all up or down at once.

## Requirements
- [django](https://www.djangoproject.com/download/)
- [django.contrib.sites](https://docs.djangoproject.com/en/1.8/ref/contrib/sites/)

## Pre-Requisites
You must have at least one Site entry in your database **before** installing django-maintenancemode-2.

## Supported Django Versions
- 1.9
- 1.8
- 1.7
- 1.6
- 1.5 or below *should* work, but proceed with caution

## Installation
1. `pip install django-maintenancemode-2`

-- or --

1. Download django-maintenancemode-2 from [source](https://github.com/alsoicode/django-maintenancemode-2/archive/master.zip)
2. *optional: Enable a virtualenv
3. Run `python setup.py install` or add `maintenancemode` to your PYTHONPATH

## Settings and Required Values
- Ensure the [Sites Framework](https://docs.djangoproject.com/en/1.8/ref/contrib/sites/) is enabled and that you have at least one entry in the Sites table.
- Add `maintenancemode.middleware.MaintenanceModeMiddleware` to your `MIDDLEWARE_CLASSES`
- Add `maintenancemode` to your `INSTALLED_APPS`
- Run `python manage.py syncdb` to create the maintenancemode tables.
- Run your project to automatically add the maintenancemode database records.

## Usage
To put a site into "Maintenance Mode", just check the "In Maintenance Mode" checkbox and save. The next time you visit the public side of the site it will return a 503 if:

- You are not a superuser / staff
- You are not viewing a URL in the ignored patterns list
- Your `REMOTE_ADDR` does not appear in the `INTERNAL_IPS` setting

Maintenance mode will create a database record per site in the Sites app. This allows you to bring each domain down independently if your project serves multiple domains.

Patterns to ignore are registered as an inline model for each maintenance record. Patterns are defined exactly the same way you write Django URLs normally.

## Testing
A test application is included "testproject" which also contains tests you can run via `python manage.py test` from the `testproject` directory.


## Database migrations
Legacy support for South migrations is supported, otherwise `manage.py syncdb` should add the necessary tables.
