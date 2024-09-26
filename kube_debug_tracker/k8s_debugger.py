# k8s_debugger.py
from kubernetes import client, config

# Cargar la configuración de Kubernetes
def load_kube_config():
    try:
        config.load_kube_config()  # Carga la configuración local (de ~/.kube/config)
        print("Kubernetes config loaded")
    except Exception as e:
        print(f"Error loading Kubernetes config: {e}")

# Obtener logs de un pod
def get_pod_logs(namespace, pod_name):
    try:
        v1 = client.CoreV1Api()
        pod_logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        return pod_logs
    except Exception as e:
        print(f"Error fetching logs for pod {pod_name}: {e}")
        return None

# Describir un pod
def describe_pod(namespace, pod_name):
    try:
        v1 = client.CoreV1Api()
        pod_desc = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
        return pod_desc
    except Exception as e:
        print(f"Error describing pod {pod_name}: {e}")
        return None
