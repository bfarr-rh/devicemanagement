#!/usr/bin/env python3

import json

inventory = {
    "_meta": {
        "hostvars": {
            "srlinux-lab-leaf-01-0": {
                "pod_name": "srlinux-lab-leaf-01-0",
                "pod_namespace": "fttx-demo"
            }
        }
    },
    "all": {
        "children": [
            "openshift_pods"
        ]
    },
    "openshift_pods": {
        "hosts": [
            "srlinux-lab-leaf-01-0"
        ]
    }
}

print(json.dumps(inventory))
