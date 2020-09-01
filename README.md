# Example of  kubernetes admission controller

## Run

Execute :
* `kubectl apply -f  manifests/01-namespace.yaml`
* `kubectl --namespace='' apply -f https://github.com/jetstack/cert-manager/releases/download/v0.9.0/cert-manager.yaml`
* `kubectl apply -f manifests/cert-manager-certificates.yaml`
* `cd controller` and `docker built -t admission:test .`
* load image  to minikube/kind
* `kubectl apply -f manifests/admission-service.yaml`
* `kubectl apply -f manifests/admission-configuration.yaml`
* `kubectl apply -f manifests/admission-configuration.yaml`


And now test:
* `kubectl apply -f manifests/99-test-namespace.yaml`