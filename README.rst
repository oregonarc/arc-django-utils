=====================
ARC Django Middleware
=====================

Installation
============

1. Clone the repo
2. Put the middleware folder in the root of your project.
3. Edit you settings.py file to incorporate the appropriate middleware

    'fish.middleware.request_user.ExceptionUserInfoMiddleware', 



ExceptionUserInfoMiddleware
---------------------------
Adds username and email address to error emails.


