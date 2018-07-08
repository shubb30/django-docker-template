# Django Docker Template

This is a starting point to create a Django app that will run in Docker.
There are a few things that need to change from the default way of running a Django app when running it in a container.

1. When running in production, Django does not serve static (css, js, images) files itself, but relies on the administrator to [serve them another way](https://docs.djangoproject.com/en/1.11/howto/static-files/deployment/) .  Normally that could be done by running an Nginx or Apache service along side the Gunicorn worker for Django.  Docker has a general rule they recommend of [one process per container](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#decouple-applications).  This template uses Docker [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/)  to create two different containers, one that will serve the app, and one that will serve the static files.  This adds the additional benefit that the app containers can be scaled differently than the static containers based on the load that they each have.

2. By default, Django places the settings.py file in the main project directory.  This is the same directory where the rest of your code is, and therefore will be commited to your source code.  This template modifies the settings file to read the values from a separate config file that can be mounted into the container via a secret.  It also retrieves the Django secret in the same location (or a different location if you choose).  The settings.py file has a variable ```CONF_LOCATION``` that must point to the location where the config is mounted as a secret.  All other config values will be read from that config file.

###Dockerfile

The Dockerfile uses ```shubb30/django-base```which is a lightweight Alpine image as a base image for the app.  Change the image name if you want to use your own custom base image.  You can also add additional packages, modules or files.

###Jenkinsfile

I use Jenkins as my CI/CD pipeline to create new continer images when I push any changes to the repo.  Jenkins will automatically build and push two image tags: one for ```app``` and ```static``` with each version.  The file ```src/VERSION.txt``` is used to differentiate the major/minor/patch version of the image name, as well as a variable within the Django settings.

###rename.sh

The ```rename.sh``` script can be used to rename all instances of ```myproject```, ```myapp```, and ```myusername``` in the example files to the names for your app.