# An example aiohttp microservice for Kubernetes

This project demonstrates a simple microservice application based on aiohttp
and designed to be deployed on Kubernetes/OpenShift.

## Instructions

```bash
# Create the Docker image
make docker
# Run the tests
docker run -t aiohttp-demo aio-demo-test
# Run the application locally
docker run -t aiohttp-demo
# Now open a browser and visit http://localhost:8080
```
