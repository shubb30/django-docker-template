# Deployment

This example is how to deploy a Django app into a Kubernetes cluster with a separate deployment for the Django app, and the static files.

Since the config file and secret file are not stored with the source code, they need to be mounted in as a secret.  In the example kubectl command, the directory ```/path/to/etc/myproject``` will have 2 files, ```settings.conf``` and ```secret.txt```.  The YYYYMM... suffix on the secret name is used to keep track of the version of the secret.  Whenever the a config is changed, a new secret should be generated, and the app deployment updated with the new secret name.

```kubectl create secret generic etc-myproject-YYYYMMDDhhmmss --from-file=/path/to/etc/myproject```

If your containers are stored in a private Docker repo, then you will need to create a Kubernetes Docker registry secret that so Kubernetes can pull from the repo.  Create a Kubetnetes Registry secret with the command:

```kubectl create secret docker-registry dockerhub --docker-username=myusername --docker-password=mypassword --docker-email=me@mydomain.com```

The ```dockerhub``` keyword is the name of the secret, and is what is referenced in the deployment yaml files.

This example uses a MySQL backend for the Django app.  A separate yaml file must be generated to create a MySQL container in the cluster, or an external database/service must be used.