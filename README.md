# OWASP ZAP DASHBOARD FOR KUBERNETER

### Install by Terraform

```tf
resource "kubernetes_namespace" "owasp-zap-dashboard" {
  metadata {
    name = "owasp-zap-dashboard"
  }
}

resource "helm_release" "owasp-zap-dashboard" {
  name = "owasp-zap-dashboard"

  repository = "https://oleksandr-mazur.github.io/helm"
  chart      = "zap-dashboard"
  version    = "0.0.2"
  namespace  = kubernetes_namespace.owasp-zap-dashboard.metadata[0].name

  values = [
    "${file("configs/owasp-zap-dashboard.yaml")}"
  ]

  depends_on = [
    kubernetes_namespace.owasp-zap-dashboard,
  ]
}
```

#### configs/owasp-zap-dashboard.yaml
```yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: owasp-zap-dashboard-tls

  hosts:
    - host: zap.devops.kyiv.ua
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls:
   - secretName: owasp-zap-dashboard-tls
     cmEmail: cf@devops.kyiv.ua
     solvers:
      - dns01:
          cloudflare:
            email: cf@devops.kyiv.ua
            apiTokenSecretRef:
              name: cloudflare-token
              key: cf_api_token
     hosts:
       - zap.devops.kyiv.ua


jobs:
  - name: "dev-frontend-app"
    schedule: "5 10 * * */2"
    endpoint: https://devops.kyiv.ua
    scanType: zap-full-scan.py

  - name: "dev-backend-app"
    schedule: "10 10 * * */2"
    endpoint: https://api.devops.kyiv.ua
    scanType: zap-api-scan.py
    args: ["-f", "openapi"]
```

### scanType
* [zap-api-scan.py](https://www.zaproxy.org/docs/docker/full-scan/)
* [zap-full-scan.py](https://www.zaproxy.org/docs/docker/api-scan/)
* [zap-baseline.py](https://www.zaproxy.org/docs/docker/baseline-scan/)