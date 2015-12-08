# django-maintenancemode-2

[![Build Status](https://travis-ci.org/alsoicode/django-maintenancemode-2.svg)](https://travis-ci.org/alsoicode/django-maintenancemode-2)

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
- 1.5 or below *should* work, but come on, it's time to upgrade :)

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

![Image of django-maintenancemode-2](https://res.cloudinary.com/alsoicode/image/upload/v1449536018/django-maintenancemode-2/maintenancemode.jpg)

To put a site into "Maintenance Mode", just check the "In Maintenance Mode" checkbox and save. The next time you visit the public side of the site it will return a 503 if:

- You are not a superuser / staff
- You are not viewing a URL in the ignored patterns list
- Your `REMOTE_ADDR` does not appear in the `INTERNAL_IPS` setting

Maintenance mode will create a database record per site in the Sites app. This allows you to bring each domain down independently if your project serves multiple domains.

Patterns to ignore are registered as an inline model for each maintenance record. Patterns are defined exactly the same way you write Django URLs normally.

## Testing and Sample Application
A "testproject" application is included which also contains unit and functional tests you can run via `python manage.py test` from the `testproject` directory.

The admin username/password is: admin

There are only two views in the testproject:
- /
- ignored-page

To see `maintenancemode` in action, log into Django admin, and set the maintenance mode to true. Log out, then visit the home page and instead, you'll be greeted with the maintenance page.

To have `maintenancemode` ignore the "ignnored-page" view, simply add it's url pattern to the Ignored URLs as:

    /ignored-page

Now you should be able to visit the `/ignored-page` view regardless of the maintenancemode status. This is useful for contact or help pages that you still want people to be able to access while you're working on other parts of the site.

### Database migrations
Legacy support for South migrations is supported, otherwise `manage.py syncdb` should add the necessary tables.
