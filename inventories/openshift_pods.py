#!/usr/bin/env python3

import json
import os
import sys

from kubernetes import client
from kubernetes.client.rest import ApiException


def get_env(name, default=None, required=False):
    value = os.environ.get(name, default)

    if required and not value:
        print(
            json.dumps({
                "error": f"Required environment variable {name} is not set"
            }),
            file=sys.stderr,
        )
        sys.exit(1)

    return value


def build_inventory():

    namespace = get_env(
        "OPENSHIFT_NAMESPACE",
        required=True
    )

    api_host = get_env(
        "K8S_AUTH_HOST",
        required=True
    )

    api_token = get_env(
        "K8S_AUTH_API_KEY",
        required=True
    )

    verify_ssl = get_env(
        "K8S_AUTH_VERIFY_SSL",
        "True"
    ).lower() == "true"

    ca_cert = os.environ.get("K8S_AUTH_SSL_CA_CERT")

    configuration = client.Configuration()

    configuration.host = api_host
    configuration.api_key = {
        "authorization": api_token
    }
    configuration.api_key_prefix = {
        "authorization": "Bearer"
    }

    configuration.verify_ssl = verify_ssl

    if ca_cert:
        configuration.ssl_ca_cert = ca_cert

    api_client = client.ApiClient(configuration)
    v1 = client.CoreV1Api(api_client)

    try:
        pods = v1.list_namespaced_pod(namespace=namespace)
    except ApiException as exc:
        print(
            f"Unable to query OpenShift API: {exc}",
            file=sys.stderr
        )
        sys.exit(1)

    inventory = {
        "_meta": {
            "hostvars": {}
        },

        "all": {
            "children": [
                "openshift_pods"
            ]
        },

        "openshift_pods": {
            "hosts": []
        }
    }

    for pod in pods.items:

        pod_name = pod.metadata.name

        inventory["openshift_pods"]["hosts"].append(
            pod_name
        )

        labels = pod.metadata.labels or {}

        inventory["_meta"]["hostvars"][pod_name] = {
            "pod_name": pod_name,
            "pod_namespace": pod.metadata.namespace,
            "pod_ip": pod.status.pod_ip,
            "pod_phase": pod.status.phase,
            "pod_node": pod.spec.node_name,
            "pod_labels": labels,

            # Important:
            # We are NOT using the Pod IP as ansible_host.
            #
            # The playbook will use k8s_exec to communicate
            # with the Pod through the Kubernetes API.
            "ansible_connection": "local"
        }

    return inventory


def main():

    if len(sys.argv) > 1:
        if sys.argv[1] in ("--list", "--export"):
            print(
                json.dumps(
                    build_inventory(),
                    indent=2
                )
            )
            return

        if sys.argv[1] == "--host":
            # AAP may ask for a specific host.
            # Host variables are already returned through _meta.
            print("{}")
            return

    print(
        json.dumps(
            build_inventory(),
            indent=2
        )
    )


if __name__ == "__main__":
    main()
