# Getting started with Django on Cloud Run

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=run/django/README.md

This repository is an example of how to run a [Django](https://www.djangoproject.com/) 
app on Google Cloud Run (fully managed). 

The Django application used in this tutorial is the [Writing your first Django app](https://docs.djangoproject.com/en/3.2/#first-steps),
after completing [Part 1](https://docs.djangoproject.com/en/3.2/intro/tutorial01/) and [Part 2](https://docs.djangoproject.com/en/3.2/intro/tutorial02/).


# Tutorial
<!-- See our [Running Django on Cloud Run (fully managed)](https://cloud.google.com/python/django/run) tutorial for instructions for setting up and deploying this sample application.


gcloud sql databases create turage --instance postgresql

-- Activate virtual environment <br>
-- Create [superuser](https://ordinarycoders.com/blog/article/django-user-register-login-logout) <br>
-- Log into the admin board [here](http://127.0.0.1:8000/admin/) using superuser credentials <br>
--  -->

Cd on the root folder of the project, and create the virtual environment with
```bash
make create_environment
```

Then, you can activate it with:
```bash
source env/bin/activate
```

And install dependencies with:
```bash
make install
```
With all dependencies installed, you can check other quick make commands from the Makefile.

Last step, make a copy of the .env.development file, and rename it to .env. Then, set values to the those environment variables

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.