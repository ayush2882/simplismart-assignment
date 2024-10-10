# simplismart-assignment

1. Understanding the Problem Statement/Requirement. The requirement was to write a script to that would connect to a minikube cluster in my case, install keda related tools, create deployment, service and hpa for event driven scaling to happen and get the status of the pods.

2. Prequisites for the assigment:

a) Minikube: A local Kubernetes cluster.
b) kubectl: To interact with the cluster.
c) Helm: Package manager for installing KEDA.
4) Python 3.x: For running the script.
5) Docker: For container image management. 

3. Ceated yaml files for deployment, service and hpa configuration.

4. Used the script to connect to the cluster, used the yaml files created in step 2 in the script to create the required components.

5. The script k8s_automation.py will install KEDA, create the deployment, apply the autoscaler, and retrieve health metrics.

6. Check the Keda Pods - `kubectl get pods -n keda`

`kubectl get pods -n keda
NAME                                               READY   STATUS    RESTARTS   AGE
keda-admission-webhooks-69d4985cfb-fhf9t           1/1     Running   0          19h
keda-operator-59b9bb47df-cswmw                     1/1     Running   0          19h
keda-operator-metrics-apiserver-5589c4f484-7k2mm   1/1     Running   0          19h`

7. Check deployment status - `kubectl get pods | grep nginx`

`kubectl get pods | grep nginx
nginx-deployment-7c79bddb59-8gsg8   1/1     Running   0             20h`

8. Checking Pod metrics - `kubectl get hpa`

`kubectl get hpa
NAME                          REFERENCE                     TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
keda-hpa-nginx-scaledobject   Deployment/nginx-deployment   cpu: 0%/50%   1         10        1          19h`

9. Simulating load to verify autoscaling - `kubectl run -i --tty load-generator --rm --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://nginx-service; done`

10. Checking the HPA at different intervals: `kubectl get hpa`

`kubectl get hpa
NAME                          REFERENCE                     TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
keda-hpa-nginx-scaledobject   Deployment/nginx-deployment   cpu: 32%/50%   1         10        1          19h`

11. `kubectl get hpa
NAME                          REFERENCE                     TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
keda-hpa-nginx-scaledobject   Deployment/nginx-deployment   cpu: 32%/50%   1         10        1          19h`

12. Now the Nginx Pods have scaled: 
`kubectl get pods
NAME                                READY   STATUS    RESTARTS      AGE
load-generator                      1/1     Running   1 (19h ago)   19h
load-generator1                     1/1     Running   0             19h
load-generator2                     1/1     Running   0             66s
nginx-deployment-7c79bddb59-8gsg8   1/1     Running   0             20h
nginx-deployment-7c79bddb59-ml8nn   1/1     Running   0             40s`

13. The nginx-pods have scaled.
