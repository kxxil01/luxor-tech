import kopf
import kubernetes.client
from kubernetes.client.rest import ApiException
import yaml


    

@kopf.on.create('luxor.tech', 'v1', 'demowebs')
def create_fn(spec, name, **kwargs):
    doc = get_yaml(spec, name, **kwargs)
    
    kopf.adopt(doc)

    # Actually create an object by requesting the Kubernetes API.
    api = kubernetes.client.AppsV1Api()
    try:
      depl = api.create_namespaced_deployment(namespace=doc['metadata']['namespace'], body=doc)
      # Update the parent's status.
      return {'children': [depl.metadata.uid]}
    except ApiException as e:
      print("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e)
    
  
@kopf.on.update('luxor.tech', 'v1', 'demowebs')
def update_fn(spec, name, **kwargs):
    doc = get_yaml(spec, name, **kwargs)
    
    kopf.adopt(doc)

    # Actually patch an object by requesting the Kubernetes API.
    api = kubernetes.client.AppsV1Api()
    try:
      depl = api.patch_namespaced_deployment(name=name+"-deployment", namespace=doc['metadata']['namespace'], body=doc)
      # Update the parent's status.
      return {'children': [depl.metadata.uid]}
    except ApiException as e:
      print("Exception when calling AppsV1Api->update_namespaced_deployment: %s\n" % e)
    

def get_yaml(spec, name, **kwargs):
    # Create the deployment spec
    doc = yaml.safe_load(f"""
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: {name}-deployment
          labels:
            app: {name}
        spec:
          replicas: {spec.get('replicas', 1)}
          selector:
            matchLabels:
              app: {name}
          template:
            metadata:
              labels:
                app: {name}
            spec:
              containers:
              - name: demoweb
                image: docker.io/library/luxor:v15
                ports:
                - containerPort: 5000
                volumeMounts:
                - name: luxor-config
                  mountPath: /python-docker/config.py
                  subPath: config.py
                  readOnly: true
              dnsPolicy: Default
              volumes:
              - name: luxor-config
                configMap:
                  name: luxor-config
    """)
    return doc