import subprocess
import os
import time

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')

def setup_kubectl():
    run_command("kubectl config use-context minikube")

def install_helm():
    print("Installing Helm...")
    run_command("helm repo add kedacore https://kedacore.github.io/charts")
    run_command("helm repo update")
    print("Installing KEDA...")
    run_command("helm install keda kedacore/keda --namespace keda --create-namespace")
    print("KEDA installed successfully.")

def verify_keda():
    result = run_command("kubectl get pods -n keda")
    print(f"KEDA status: {result}")

def apply_yaml_files():
    print("Applying deployment.yaml...")
    run_command("kubectl apply -f nginx-deployment.yaml")
    
    print("Applying service.yaml...")
    run_command("kubectl apply -f nginx-service.yaml")
    
    print("Applying keda-hpa.yaml...")
    run_command("kubectl apply -f keda-hpa.yaml")

def get_deployment_status(deployment_name):
    print(f"Checking status of deployment: {deployment_name}...")
    result = run_command(f"kubectl get deployment {deployment_name}")
    print(result)

def get_pod_metrics():
    print("Getting pod metrics...")
    result = run_command("kubectl top pods")
    print(result)

if __name__ == "__main__":
    try:
        print("Setting up kubectl for Minikube...")
        setup_kubectl()

        print("Installing KEDA via Helm...")
        install_helm()

        print("Verifying KEDA installation...")
        verify_keda()

        print("Applying Kubernetes resources (Deployment, Service, HPA)...")
        apply_yaml_files()

        print("Waiting for deployment to stabilize...")
        time.sleep(10)

        print("Retrieving deployment health status...")
        get_deployment_status("nginx-deployment")

        print("Retrieving pod metrics...")
        get_pod_metrics()

        print("Script executed successfully.")

    except Exception as e:
        print(f"Error: {e}")