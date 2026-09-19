# Kubernetes + GitHub Actions Practical Guide

> This tutorial is aimed at Chinese developers, systematically explaining how to deeply integrate Kubernetes with GitHub Actions to achieve a fully automated pipeline from code commit to production deployment.

---

## Table of Contents

1. [Kubernetes Basic Concepts Review](#1-kubernetes-basic-concepts-review)
2. [GitHub Actions Deployment to K8s Solutions](#2-github-actions-deployment-to-k8s-solutions)
3. [kubectl Configuration and GitHub Secrets](#3-kubectl-configuration-and-github-secrets)
4. [Helm Chart + GitHub Actions Deployment](#4-helm-chart--github-actions-deployment)
5. [Kustomize + GitHub Actions Deployment](#5-kustomize--github-actions-deployment)
6. [ArgoCD + GitOps Workflow](#6-argocd--gitops-workflow)
7. [Flux CD + GitHub Integration](#7-flux-cd--github-integration)
8. [K8s Multi-Environment Management (dev/staging/prod)](#8-k8s-multi-environment-management-devstagingprod)
9. [K8s Autoscaling Configuration](#9-k8s-autoscaling-configuration)
10. [Monitoring and Alerting (Prometheus + Grafana)](#10-monitoring-and-alerting-prometheus--grafana)
11. [K8s Security Best Practices](#11-k8s-security-best-practices)
12. [Cloud Provider K8s Services](#12-cloud-provider-k8s-services)
13. [K8s Cost Optimization](#13-k8s-cost-optimization)
14. [Domestic K8s Deployment Considerations](#14-domestic-k8s-deployment-considerations)

---

## 1. Kubernetes Basic Concepts Review

### 1.1 What is Kubernetes

Kubernetes (abbreviated as K8s) is an open-source container orchestration platform by Google, used for automating deployment, scaling, and management of containerized applications. It has become the de facto standard in the cloud-native field and is widely adopted by major enterprises both domestically and internationally.

### 1.2 Core Architecture

Kubernetes adopts a master-slave architecture, mainly consisting of the following components:

**Control Plane:**

- `kube-apiserver`: API server, the entry point for all operations
- `etcd`: Distributed key-value store, saves cluster state
- `kube-scheduler`: Scheduler, decides which node a Pod runs on
- `kube-controller-manager`: Controller manager, maintains desired state

**Worker Node:**

- `kubelet`: Node agent, manages Pod lifecycle
- `kube-proxy`: Network proxy, implements Service load balancing
- `Container Runtime`: Container runtime (Docker, containerd, CRI-O)

### 1.3 Core Resource Objects

```yaml
# Pod - Minimum deployment unit
apiVersion: v1
kind: Pod
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  containers:
  - name: my-app
    image: my-registry.com/my-app:v1.0.0
    ports:
    - containerPort: 8080
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
---
# Deployment - Stateless application deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-registry.com/my-app:v1.0.0
        ports:
        - containerPort: 8080
---
# Service - Service discovery and load balancing
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
---
# Ingress - HTTP routing
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: my-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-app-service
            port:
              number: 80
```

### 1.4 Kubernetes Object Management Methods

| Method | Description | Use Case |
|------|------|----------|
| Imperative Commands | `kubectl run/create/delete` | Ad-hoc testing |
| Imperative Object Configuration | `kubectl create -f manifest.yaml` | Simple deployments |
| Declarative Object Configuration | `kubectl apply -f manifest.yaml` | Production environments (recommended) |

### 1.5 Why Choose Kubernetes + GitHub Actions

Advantages of GitHub Actions as a CI/CD platform:

- **Native Integration**: Seamless integration with GitHub repositories, triggered on code push
- **Rich Ecosystem**: Marketplace provides thousands of ready-made Actions
- **Matrix Builds**: Supports parallel testing across multiple platforms and versions
- **Self-hosted Runner**: Can run Runners in internal K8s clusters
- **Security Mechanisms**: Comprehensive security system with Secrets, OIDC, environment approvals, etc.

---

## 2. GitHub Actions Deployment to K8s Solutions

### 2.1 Common Deployment Solution Comparison

| Solution | Complexity | Security | Use Case |
|------|--------|--------|----------|
| kubectl Direct Deployment | Low | Medium | Small projects, quick validation |
| Helm Chart Deployment | Medium | Medium | Medium to large projects, multi-environment |
| Kustomize Deployment | Medium | Medium | Multi-environment variant management |
| ArgoCD (GitOps) | High | High | Enterprise production environments |
| Flux CD (GitOps) | High | High | Enterprise production environments |

### 2.2 Basic Pipeline Architecture

```
Code Commit → GitHub Actions CI → Build Image → Push Image Registry → Deploy to K8s
    ↓              ↓              ↓            ↓              ↓
  Trigger      Test/Scan      Docker Build   Alibaba Cloud ACR/   kubectl/Helm
                                                Tencent Cloud CCR/
                                                Huawei Cloud SWR
```

### 2.3 Complete CI/CD Pipeline Example

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: registry.cn-hangzhou.aliyuncs.com
  NAMESPACE: my-namespace
  IMAGE_NAME: my-app

jobs:
  # Stage 1: Code Testing
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Go
      uses: actions/setup-go@v5
      with:
        go-version: '1.22'
    
    - name: Run tests
      run: go test -v -race -coverprofile=coverage.out ./...
    
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage.out

  # Stage 2: Build and Push Image
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to Alibaba Cloud ACR
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ secrets.ACR_USERNAME }}
        password: ${{ secrets.ACR_PASSWORD }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.NAMESPACE }}/${{ env.IMAGE_NAME }}
        tags: |
          type=sha,prefix=
          type=ref,event=branch
          type=semver,pattern={{version}}
    
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # Stage 3: Deploy to Kubernetes
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'v1.29.0'
    
    - name: Configure kubeconfig
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > $HOME/.kube/config
        chmod 600 $HOME/.kube/config
    
    - name: Deploy to K8s
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        kubectl set image deployment/my-app \
          my-app=${{ env.REGISTRY }}/${{ env.NAMESPACE }}/${{ env.IMAGE_NAME }}:${IMAGE_TAG} \
          -n production
        kubectl rollout status deployment/my-app -n production --timeout=300s
    
    - name: Notify on success
      if: success()
      run: |
        # Send DingTalk/Feishu/WeCom notification
        curl -X POST "${{ secrets.DINGTALK_WEBHOOK }}" \
          -H 'Content-Type: application/json' \
          -d '{"msgtype":"text","text":{"content":"Deployment successful: '${{ github.repository }}' @ '${GITHUB_SHA::8}'"}}'
```

---

## 3. kubectl Configuration and GitHub Secrets

### 3.1 Obtain kubeconfig

**Method 1: Get from Cloud Provider Console**

Using Alibaba Cloud ACK as an example:

```bash
# Install aliyun CLI
curl -O https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz
tar xzvf aliyun-cli-linux-latest-amd64.tgz
sudo mv aliyun /usr/local/bin/

# Configure Alibaba Cloud account
aliyun configure

# Get cluster kubeconfig
aliyun cs GET /k8s/{cluster_id}/user_config | jq -r '.config' > kubeconfig.yaml
```

**Method 2: Configure using kubectl directly**

```bash
# Alibaba Cloud ACK
aliyun cs GET /k8s/{cluster_id}/user_config | jq -r '.config' > ~/.kube/config

# Tencent Cloud TKE
# Download kubeconfig from console or use tke CLI tool

# Huawei Cloud CCE
# Download kubeconfig file from console
```

**Method 3: Use OIDC Token (more secure)**

```yaml
# Use aws-iam-authenticator (EKS)
# Use gcp-auth-plugin (GKE)
# Use OIDC Token
```

### 3.2 Configure GitHub Secrets

Set Secrets in the GitHub repository:

1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add the following Secrets:

| Secret Name | Description | How to Obtain |
|-------------|------|----------|
| `KUBECONFIG` | Base64 encoded kubeconfig | `cat ~/.kube/config \| base64 -w 0` |
| `ACR_USERNAME` | Image registry username | Alibaba Cloud Console |
| `ACR_PASSWORD` | Image registry password | Alibaba Cloud Console |
| `SLACK_WEBHOOK` | Notification Webhook | Slack/DingTalk/Feishu Settings |

### 3.3 Base64 Encode kubeconfig

```bash
# Linux
cat ~/.kube/config | base64 -w 0

# macOS
cat ~/.kube/config | base64

# Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("$env:USERPROFILE\.kube\config"))
```

### 3.4 Use GitHub Environments to Manage Multiple Environments

```yaml
# Create environment: Settings → Environments → New environment
# - development
# - staging
# - production (add approval rules)

jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
    - name: Deploy
      run: kubectl apply -f k8s/prod/
```

### 3.5 Use OIDC Instead of Long-Term Credentials (Recommended)

GitHub Actions supports OIDC (OpenID Connect) federation with cloud providers, avoiding storing long-term credentials:

```yaml
# Alibaba Cloud OIDC Configuration
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    
    steps:
    - name: Configure Alibaba Cloud credentials
      uses: aliyun/oss-upload-action@v1
      with:
        access-key-id: ${{ secrets.ALIYUN_ACCESS_KEY_ID }}
        access-key-secret: ${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}
    
    # Or use OIDC (more secure)
    - name: Assume Role via OIDC
      run: |
        # Get OIDC Token
        OIDC_TOKEN=$(curl -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
          "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=sts.aliyuncs.com" | jq -r '.value')
        
        # Use STS Assume Role
        aliyun sts AssumeRoleWithOIDC \
          --RoleArn "acs:ram::123456789:role/github-actions-role" \
          --OIDCProviderArn "acs:ram::123456789:oidc-provider/github" \
          --OIDCToken "$OIDC_TOKEN" \
          --RoleSessionName "github-actions"
```

**AWS EKS OIDC Configuration Example:**

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    
    steps:
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789012:role/github-actions-role
        aws-region: cn-northwest-1
    
    - name: Update kubeconfig
      run: aws eks update-kubeconfig --name my-cluster --region cn-northwest-1
```

---

## 4. Helm Chart + GitHub Actions Deployment

### 4.1 Helm Basic Concepts

Helm is the package manager for Kubernetes, packaging related resources into Charts:

```
my-chart/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── templates/          # Template files
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   └── _helpers.tpl
├── charts/             # Dependent sub-charts
└── README.md
```

### 4.2 Create Helm Chart

```bash
# Create new Chart
helm create my-app

# Chart.yaml
cat > my-app/Chart.yaml << 'EOF'
apiVersion: v2
name: my-app
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
- name: postgresql
  version: "12.x.x"
  repository: "https://charts.bitnami.com/bitnami"
  condition: postgresql.enabled
EOF
```

### 4.3 values.yaml Multi-Environment Configuration

```yaml
# values.yaml - Default values
replicaCount: 1

image:
  repository: registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: nginx
  annotations: {}
  hosts:
  - host: my-app.local
    paths:
    - path: /
      pathType: Prefix

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

nodeSelector: {}
tolerations: []
affinity: {}
```

```yaml
# values-production.yaml - Production environment overrides
replicaCount: 3

image:
  tag: ""  # Set dynamically by CI/CD

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
  - host: my-app.example.com
    paths:
    - path: /
      pathType: Prefix
  tls:
  - secretName: my-app-tls
    hosts:
    - my-app.example.com

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: "2"
    memory: 2Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70

postgresql:
  enabled: true
  auth:
    existingSecret: postgres-credentials
```

### 4.4 GitHub Actions Helm Deployment Workflow

```yaml
name: Helm Deploy

on:
  push:
    branches: [main]

env:
  RELEASE_NAME: my-app
  NAMESPACE: production
  CHART_PATH: ./helm/my-app

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Helm
      uses: azure/setup-helm@v3
      with:
        version: 'v3.14.0'
    
    - name: Configure kubectl
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > $HOME/.kube/config
    
    - name: Add Helm repos
      run: |
        helm repo add bitnami https://charts.bitnami.com/bitnami
        helm repo update
    
    - name: Update Chart dependencies
      run: |
        helm dependency update ${{ env.CHART_PATH }}
    
    - name: Helm Lint
      run: |
        helm lint ${{ env.CHART_PATH }} -f ${{ env.CHART_PATH }}/values-production.yaml
    
    - name: Helm Diff (dry-run)
      run: |
        helm diff upgrade ${{ env.RELEASE_NAME }} ${{ env.CHART_PATH }} \
          -f ${{ env.CHART_PATH }}/values-production.yaml \
          --namespace ${{ env.NAMESPACE }} \
          --allow-unreleased || true
    
    - name: Deploy with Helm
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        helm upgrade --install ${{ env.RELEASE_NAME }} ${{ env.CHART_PATH }} \
          -f ${{ env.CHART_PATH }}/values-production.yaml \
          --namespace ${{ env.NAMESPACE }} \
          --create-namespace \
          --set image.tag=${IMAGE_TAG} \
          --wait \
          --timeout 5m
    
    - name: Verify deployment
      run: |
        kubectl rollout status deployment/${{ env.RELEASE_NAME }} \
          -n ${{ env.NAMESPACE }} --timeout=300s
        kubectl get pods -n ${{ env.NAMESPACE }} -l app.kubernetes.io/name=my-app
```

### 4.5 Helm Chart Testing

```yaml
# Run Helm tests in GitHub Actions
- name: Run Helm tests
  run: |
    helm test ${{ env.RELEASE_NAME }} -n ${{ env.NAMESPACE }} --timeout 5m
```

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-app.fullname" . }}-test-connection"
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: wget
    image: busybox
    command: ['wget']
    args: ['{{ include "my-app.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

---

## 5. Kustomize + GitHub Actions Deployment

### 5.1 Kustomize Introduction

Kustomize is a Kubernetes native configuration management tool that achieves multi-environment configuration management through the overlay mechanism, without needing a template engine.

### 5.2 Project Structure

```
k8s/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── namespace.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   ├── replica-count.yaml
    │   └── resource-limits.yaml
    └── prod/
        ├── kustomization.yaml
        ├── replica-count.yaml
        ├── resource-limits.yaml
        └── hpa.yaml
```

### 5.3 Base Configuration

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

commonLabels:
  app: my-app
  managed-by: kustomize

resources:
- deployment.yaml
- service.yaml
- ingress.yaml

configMapGenerator:
- name: app-config
  literals:
  - APP_ENV=production
  - LOG_LEVEL=info

secretGenerator:
- name: app-secrets
  type: Opaque
  literals:
  - DB_PASSWORD=changeme

images:
- name: my-app
  newName: registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app
  newTag: latest
```

```yaml
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
```

### 5.4 Overlay Configuration

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
- ../../base
- hpa.yaml

patches:
- path: replica-count.yaml
- path: resource-limits.yaml

configMapGenerator:
- name: app-config
  behavior: merge
  literals:
  - APP_ENV=production
  - LOG_LEVEL=warn

images:
- name: my-app
  newTag: ""  # Set dynamically by CI/CD
```

```yaml
# overlays/prod/replica-count.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 5
```

```yaml
# overlays/prod/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 5.5 Kustomize + GitHub Actions Workflow

```yaml
name: Kustomize Deploy

on:
  push:
    branches: [main]

env:
  IMAGE: registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
    
    - name: Configure kubeconfig
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > $HOME/.kube/config
    
    - name: Set image tag
      id: tag
      run: echo "tag=${GITHUB_SHA::8}" >> $GITHUB_OUTPUT
    
    - name: Kustomize build and apply
      run: |
        cd k8s/overlays/prod
        
        # Use kustomize edit to set image tag
        kustomize edit set image my-app=${{ env.IMAGE }}:${{ steps.tag.outputs.tag }}
        
        # Build and apply
        kustomize build . | kubectl apply -f -
        
        # Wait for deployment to complete
        kubectl rollout status deployment/my-app -n production --timeout=300s
```

### 5.6 Using kubectl's Built-in Kustomize

```yaml
# Use kubectl apply -k directly
- name: Deploy with kubectl kustomize
  run: |
    cd k8s/overlays/prod
    kustomize edit set image my-app=${{ env.IMAGE }}:${{ steps.tag.outputs.tag }}
    kubectl apply -k .
```

---

## 6. ArgoCD + GitOps Workflow

### 6.1 GitOps Principles

GitOps is an operational model where the Git repository is the single source of truth:

1. **Declarative**: All configurations are stored declaratively in Git
2. **Versioned**: All changes are tracked through Git
3. **Automated**: Changes are automatically applied to the cluster
4. **Self-healing**: Automatically repairs when cluster state diverges from Git declarations

### 6.2 ArgoCD Architecture

```
Git Repository (Desired State)
        ↓
   ArgoCD Server
        ↓
   Application Controller → Kubernetes Cluster (Actual State)
        ↓
   Notification Controller → DingTalk/Feishu/Slack
```

### 6.3 Install ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get initial password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Access UI (port forwarding)
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Install CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
```

### 6.4 ArgoCD Application Configuration

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/my-org/my-app-config.git
    targetRevision: HEAD
    path: overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true        # Delete resources that don't exist in Git
      selfHeal: true     # Automatically repair manual changes
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### 6.5 GitHub Actions + ArgoCD Integration

**Method 1: ArgoCD Auto-detects Git Changes (Pull Mode)**

ArgoCD checks Git repository changes every 3 minutes by default, no additional configuration needed.

**Method 2: GitHub Actions Triggers ArgoCD Sync (Push Mode)**

```yaml
name: Build and Notify ArgoCD

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Build and push image
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        docker build -t registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app:${IMAGE_TAG} .
        docker push registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app:${IMAGE_TAG}
    
    - name: Update image tag in config repo
      run: |
        # Clone config repository
        git clone https://x-access-token:${{ secrets.CONFIG_REPO_TOKEN }}@github.com/my-org/my-app-config.git
        cd my-app-config
        
        # Update image tag
        cd overlays/prod
        kustomize edit set image my-app=registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app:${GITHUB_SHA::8}
        
        # Commit and push
        git config user.name "GitHub Actions"
        git config user.email "actions@github.com"
        git add .
        git commit -m "Update image to ${GITHUB_SHA::8}"
        git push
    
    - name: Trigger ArgoCD sync
      run: |
        # Method 1: Use ArgoCD CLI
        argocd app sync my-app --server argocd.example.com \
          --auth-token ${{ secrets.ARGOCD_TOKEN }} \
          --insecure
        
        # Method 2: Use ArgoCD API
        curl -X POST "https://argocd.example.com/api/v1/applications/my-app/sync" \
          -H "Authorization: Bearer ${{ secrets.ARGOCD_TOKEN }}" \
          -H "Content-Type: application/json" \
          -d '{}' --insecure
```

### 6.6 ArgoCD Notifications

```yaml
# Configure ArgoCD notifications
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.webhook.dingtalk: |
    url: https://oapi.dingtalk.com/robot/send?access_token=xxx
    headers:
    - name: Content-Type
      value: application/json
  
  template.app-sync-succeeded: |
    webhook:
      dingtalk:
        method: POST
        body: |
          {
            "msgtype": "markdown",
            "markdown": {
              "title": "ArgoCD Deployment Notification",
              "text": "## ArgoCD Deployment Successful\n\n- **Application**: {{.app.metadata.name}}\n- **Status**: {{.app.status.sync.status}}\n- **Commit**: {{.app.status.sync.revision}}"
            }
          }
  
  trigger.on-sync-succeeded: |
    - when: app.status.operationState.phase in ['Succeeded']
      send: [app-sync-succeeded]
```

---

## 7. Flux CD + GitHub Integration

### 7.1 Flux CD Introduction

Flux CD is a CNCF graduated project, natively supports GitOps, and deeply integrates with the Kubernetes API.

### 7.2 Install Flux CD

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Check if cluster meets requirements
flux check --pre

# Bootstrap Flux (using GitHub as example)
flux bootstrap github \
  --owner=my-org \
  --repository=my-cluster-config \
  --branch=main \
  --path=clusters/production \
  --personal
```

### 7.3 Flux GitRepository Configuration

```yaml
# git-repository.yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/my-org/my-app-config.git
  ref:
    branch: main
  secretRef:
    name: github-credentials
```

### 7.4 Flux Kustomization Configuration

```yaml
# kustomization.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./overlays/prod
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-app
  healthChecks:
  - apiVersion: apps/v1
    kind: Deployment
    name: my-app
    namespace: production
  timeout: 3m
```

### 7.5 GitHub Actions + Flux Integration

```yaml
name: Update Flux Image

on:
  push:
    branches: [main]

jobs:
  update-image:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Flux CLI
      uses: fluxcd/flux2/action@main
    
    - name: Update image in config repo
      run: |
        IMAGE_TAG=${GITHUB_SHA::8}
        flux create image policy my-app \
          --image=my-app \
          --select-semver=">=1.0.0" \
          --interval=5m \
          --export > policy.yaml
        
        # Or use flux command directly to update
        flux update kustomization my-app \
          --source=GitRepository/my-app
```

### 7.6 Flux Image Automation

```yaml
# image-repository.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImageRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  image: registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app
  interval: 5m

---
# image-policy.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta2
kind: ImagePolicy
metadata:
  name: my-app
  namespace: flux-system
spec:
  imageRepositoryRef:
    name: my-app
  policy:
    semver:
      range: ">=1.0.0"
```

---

## 8. K8s Multi-Environment Management (dev/staging/prod)

### 8.1 Environment Management Strategies

| Strategy | Description | Use Case |
|------|------|----------|
| Single Cluster Multi-Namespace | One cluster isolated by Namespace | Cost-sensitive, small teams |
| Multi-Cluster | Each environment has independent clusters | High security requirements, large teams |
| Hybrid Mode | dev/staging in same cluster, prod independent | Balance cost and security |

### 8.2 GitHub Actions Multi-Environment Deployment

```yaml
name: Multi-Environment Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Development environment - Auto-deploy on develop branch
  deploy-dev:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: development
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to Dev
      run: |
        kubectl config use-context dev-cluster
        kustomize build k8s/overlays/dev | kubectl apply -f -
        kubectl rollout status deployment/my-app -n development

  # Staging environment - Auto-deploy on main branch
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [test, build]
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to Staging
      run: |
        kubectl config use-context staging-cluster
        kustomize build k8s/overlays/staging | kubectl apply -f -
        kubectl rollout status deployment/my-app -n staging
    
    - name: Run integration tests
      run: |
        # Run integration tests
        npm run test:integration -- --base-url=https://staging.example.com

  # Production environment - Tag triggered, requires approval
  deploy-prod:
    runs-on: ubuntu-latest
    needs: [deploy-staging]
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production  # Requires manual approval
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to Production
      run: |
        kubectl config use-context prod-cluster
        kustomize build k8s/overlays/prod | kubectl apply -f -
        kubectl rollout status deployment/my-app -n production
    
    - name: Notify success
      run: |
        curl -X POST "${{ secrets.DINGTALK_WEBHOOK }}" \
          -H 'Content-Type: application/json' \
          -d '{"msgtype":"text","text":{"content":"Production deployment successful: ${{ github.ref_name }}"}}'
```

### 8.3 Use Matrix Strategy for Multi-Environment Deployment

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging]
        include:
        - environment: dev
          namespace: development
          replicas: 1
        - environment: staging
          namespace: staging
          replicas: 2
    
    environment: ${{ matrix.environment }}
    
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to ${{ matrix.environment }}
      run: |
        kustomize build k8s/overlays/${{ matrix.environment }} | kubectl apply -f -
        kubectl scale deployment/my-app --replicas=${{ matrix.replicas }} -n ${{ matrix.namespace }}
```

### 8.4 Environment Configuration Management

```yaml
# Use GitHub Environments to configure environment variables
# Settings → Environments → Select environment → Environment variables

# Use in workflow
- name: Use environment config
  run: |
    echo "Deploying to ${{ vars.CLUSTER_NAME }}"
    echo "Namespace: ${{ vars.NAMESPACE }}"
    echo "Replicas: ${{ vars.REPLICAS }}"
```

---

## 9. K8s Autoscaling Configuration

### 9.1 HPA (Horizontal Pod Autoscaler)

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: 1000
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Pods
        value: 4
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

### 9.2 VPA (Vertical Pod Autoscaler)

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: my-app
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 4
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
```

### 9.3 Cluster Autoscaler

```yaml
# Alibaba Cloud ACK cluster autoscaling configuration
# Configure node pool autoscaling strategy in ACK console

# AWS EKS Cluster Autoscaler
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      containers:
      - image: registry.aliyuncs.com/acs/autoscaler:v1.26.3-eks
        name: cluster-autoscaler
        command:
        - ./cluster-autoscaler
        - --v=4
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/my-cluster
```

### 9.4 KEDA (Kubernetes Event-Driven Autoscaling)

```yaml
# Install KEDA
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace

# ScaledObject configuration
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: my-app
spec:
  scaleTargetRef:
    name: my-app
  minReplicaCount: 1
  maxReplicaCount: 100
  triggers:
  - type: kafka
    metadata:
      bootstrapServers: kafka:9092
      consumerGroup: my-group
      topic: my-topic
      lagThreshold: "100"
  - type: redis
    metadata:
      address: redis:6379
      listName: my-queue
      listLength: "10"
```

---

## 10. Monitoring and Alerting (Prometheus + Grafana)

### 10.1 Prometheus Installation

```bash
# Install kube-prometheus-stack using Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=your-password \
  --set prometheus.prometheusSpec.retention=30d
```

### 10.2 Custom ServiceMonitor

```yaml
# service-monitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-app
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
```

### 10.3 PrometheusRule Alert Rules

```yaml
# alert-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: my-app-alerts
  labels:
    release: prometheus
spec:
  groups:
  - name: my-app
    rules:
    - alert: HighErrorRate
      expr: |
        rate(http_requests_total{service="my-app", status=~"5.."}[5m])
        / rate(http_requests_total{service="my-app"}[5m]) > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "High Error Rate Alert"
        description: "my-app 5xx error rate exceeds 5%, current value: {{ $value }}"
    
    - alert: HighLatency
      expr: |
        histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="my-app"}[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High Latency Alert"
        description: "my-app P95 latency exceeds 1 second, current value: {{ $value }}"
    
    - alert: PodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total{namespace="production"}[15m]) > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Pod Restart Alert"
        description: "Pod {{ $labels.pod }} is frequently restarting"
```

### 10.4 Grafana Dashboard Configuration

```yaml
# grafana-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-app-dashboard
  labels:
    grafana_dashboard: "1"
data:
  my-app.json: |
    {
      "dashboard": {
        "title": "My App Dashboard",
        "panels": [
          {
            "title": "Request Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total{service=\"my-app\"}[5m])",
                "legendFormat": "{{method}} {{status}}"
              }
            ]
          },
          {
            "title": "Latency Distribution",
            "type": "heatmap",
            "targets": [
              {
                "expr": "rate(http_request_duration_seconds_bucket{service=\"my-app\"}[5m])",
                "legendFormat": "{{le}}"
              }
            ]
          }
        ]
      }
    }
```

### 10.5 GitHub Actions Deploy Monitoring Stack

```yaml
name: Deploy Monitoring Stack

on:
  push:
    branches: [main]
    paths:
    - 'monitoring/**'

jobs:
  deploy-monitoring:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      run: |
        mkdir -p $HOME/.kube
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > $HOME/.kube/config
    
    - name: Deploy Prometheus
      run: |
        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
        helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
          --namespace monitoring \
          --create-namespace \
          -f monitoring/values.yaml \
          --wait
    
    - name: Apply custom rules
      run: |
        kubectl apply -f monitoring/alert-rules.yaml
        kubectl apply -f monitoring/service-monitors.yaml
        kubectl apply -f monitoring/dashboards/
```

---

## 11. K8s Security Best Practices

### 11.1 RBAC Configuration

```yaml
# rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-app-rolebinding
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app-sa
  namespace: production
roleRef:
  kind: Role
  name: my-app-role
  apiGroup: rbac.authorization.k8s.io
```

**GitHub Actions Least Privilege:**

```yaml
# Create dedicated ServiceAccount for GitHub Actions
apiVersion: v1
kind: ServiceAccount
metadata:
  name: github-actions-deployer
  namespace: production
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: github-actions-deployer-role
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "update", "patch"]
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "create", "update"]
```

### 11.2 NetworkPolicy

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: my-app-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: my-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to:  # Allow DNS queries
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
```

### 11.3 Pod Security Standards

```yaml
# pod-security.yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: my-app
    image: my-app:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```

### 11.4 Image Security Scanning

```yaml
# Integrate Trivy scanning in GitHub Actions
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'my-app:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'  # Fail when high-risk vulnerabilities are found

- name: Upload Trivy scan results
  uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: 'trivy-results.sarif'
```

### 11.5 Sealed Secrets

```bash
# Install Sealed Secrets
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Install kubeseal CLI
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-0.24.0-linux-amd64.tar.gz
tar xvfz kubeseal-0.24.0-linux-amd64.tar.gz
sudo mv kubeseal /usr/local/bin/

# Create Sealed Secret
echo -n mypassword | kubectl create secret generic my-secret \
  --dry-run=client --from-file=password=/dev/stdin -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml
```

---

## 12. Cloud Provider K8s Services

### 12.1 Alibaba Cloud ACK (Container Service for Kubernetes)

**Create Cluster:**

```bash
# Use aliyun CLI to create ACK cluster
aliyun cs POST /clusters --header "Content-Type=application/json" --body '{
  "name": "my-cluster",
  "cluster_type": "ManagedKubernetes",
  "region_id": "cn-hangzhou",
  "kubernetes_version": "1.28.9-aliyun.1",
  "worker_instance_types": ["ecs.g6.large"],
  "num_of_nodes": 3,
  "pod_cidr": "172.20.0.0/16",
  "service_cidr": "172.21.0.0/20"
}'
```

**Configure GitHub Actions:**

```yaml
- name: Setup kubeconfig for ACK
  run: |
    # Use Alibaba Cloud OIDC or AccessKey
    aliyun cs GET /k8s/${{ secrets.ACK_CLUSTER_ID }}/user_config | jq -r '.config' > kubeconfig.yaml
    export KUBECONFIG=kubeconfig.yaml
    kubectl get nodes
```

### 12.2 Tencent Cloud TKE (Tencent Kubernetes Engine)

```yaml
# Use Tencent Cloud CLI to configure
- name: Configure TKE
  run: |
    # Install tke CLI tool
    pip install tencentcloud-sdk-python
    
    # Configure kubeconfig
    # Download from console or obtain via API
    echo "${{ secrets.TKE_KUBECONFIG }}" | base64 -d > $HOME/.kube/config
```

### 12.3 Huawei Cloud CCE (Cloud Container Engine)

```yaml
# Use Huawei Cloud CLI to configure
- name: Configure CCE
  run: |
    # Install cce CLI tool
    pip install huaweicloudsdkcce
    
    # Configure kubeconfig
    echo "${{ secrets.CCE_KUBECONFIG }}" | base64 -d > $HOME/.kube/config
```

### 12.4 Multi-Cloud Deployment Strategy

```yaml
# Use GitHub Actions Matrix for multi-cloud deployment
jobs:
  deploy-multi-cloud:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        cloud: [alibaba, tencent, huawei]
        include:
        - cloud: alibaba
          cluster: ack-cluster
          registry: registry.cn-hangzhou.aliyuncs.com
        - cloud: tencent
          cluster: tke-cluster
          registry: ccr.ccs.tencentyun.com
        - cloud: huawei
          cluster: cce-cluster
          registry: swr.cn-north-4.myhuaweicloud.com
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to ${{ matrix.cloud }}
      run: |
        # Configure corresponding cloud provider credentials
        echo "${{ secrets[format('{0}_KUBECONFIG', matrix.cloud)] }}" | base64 -d > $HOME/.kube/config
        
        # Deploy
        kubectl apply -f k8s/
```

---

## 13. K8s Cost Optimization

### 13.1 Resource Quota Management

```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    pods: "50"
    services: "20"
    persistentvolumeclaims: "10"
```

### 13.2 LimitRange Configuration

```yaml
# limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: production
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
    type: Container
```

### 13.3 Cost Monitoring

```yaml
# Use kubecost for cost monitoring
helm install kubecost cost-analyzer \
  --repo https://kubecost.github.io/cost-analyzer/ \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="your-token"
```

### 13.4 Node Optimization Strategy

```yaml
# Use Spot/Preemptible instances
# Alibaba Cloud preemptible instance configuration
apiVersion: v1
kind: Node
metadata:
  labels:
    node-type: spot
spec:
  taints:
  - key: spot
    value: "true"
    effect: NoSchedule

# Pod toleration configuration
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  tolerations:
  - key: spot
    operator: Equal
    value: "true"
    effect: NoSchedule
  nodeSelector:
    node-type: spot
```

### 13.5 GitHub Actions Cost Optimization

```yaml
# Use cache to reduce build time
- name: Cache Docker layers
  uses: actions/cache@v4
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-

# Use self-hosted Runner to reduce costs
jobs:
  build:
    runs-on: self-hosted  # Use self-hosted Runner
    steps:
    - uses: actions/checkout@v4
```

---

## 14. Domestic K8s Deployment Considerations

### 14.1 Image Acceleration Configuration

```yaml
# Configure Docker image accelerator
# /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://registry.cn-hangzhou.aliyuncs.com",
    "https://hub-mirror.c.163.com"
  ]
}
```

### 14.2 Use Domestic Image Registries

```yaml
# Alibaba Cloud Container Image Service
image: registry.cn-hangzhou.aliyuncs.com/my-namespace/my-app:v1.0.0

# Tencent Cloud Container Image Service
image: ccr.ccs.tencentyun.com/my-namespace/my-app:v1.0.0

# Huawei Cloud Container Image Service
image: swr.cn-north-4.myhuaweicloud.com/my-namespace/my-app:v1.0.0
```

### 14.3 Use Domestic Helm Repositories

```bash
# Alibaba Cloud Helm repository
helm repo add aliyun https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts

# Microsoft China mirror
helm repo add azurecn-mirror https://kubernetesartifacts.azureedge.net/stable

# Tencent Cloud Helm repository
helm repo add tencentcloud https://mirror.ccs.tencentyun.com
```

### 14.4 Resolve GitHub Access Issues

```yaml
# Use domestic Git repository mirrors
# Gitee mirrors sync GitHub repositories

# Or use proxy
- name: Git proxy
  run: |
    git config --global http.proxy http://proxy.example.com:8080
    git config --global https.proxy http://proxy.example.com:8080

# Use ghproxy to accelerate downloads
- name: Download binary
  run: |
    wget https://ghproxy.com/https://github.com/owner/repo/releases/download/v1.0.0/binary-linux-amd64
```

### 14.5 Domestic CI/CD Alternatives

| Platform | Description | Features |
|------|------|------|
| Yunxiao (Alibaba Cloud) | Alibaba Cloud DevOps platform | Deep integration with Alibaba Cloud services |
| CODING (Tencent Cloud) | Tencent Cloud DevOps platform | Deep integration with Tencent Cloud services |
| Huawei Cloud DevCloud | Huawei Cloud DevOps platform | Deep integration with Huawei Cloud services |
| Gitee Go | Gitee CI/CD | Integrated with Gitee |
| Jenkins | Open-source CI/CD | Self-hosted, flexible |

### 14.6 Compliance and Data Security

```yaml
# Data residency requirements
# - Ensure K8s cluster is deployed in domestic regions
# - Use domestic nodes for image registries
# - Store logs and monitoring data domestically

# Alibaba Cloud region selection
region: cn-hangzhou   # Hangzhou
region: cn-shanghai   # Shanghai
region: cn-beijing    # Beijing
region: cn-shenzhen   # Shenzhen
region: cn-guangzhou  # Guangzhou
region: cn-chengdu    # Chengdu

# Tencent Cloud region selection
region: ap-guangzhou  # Guangzhou
region: ap-shanghai   # Shanghai
region: ap-beijing    # Beijing
region: ap-nanjing    # Nanjing
```

---

## Appendix: Complete Project Structure Example

```
my-k8s-app/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Continuous Integration
│       ├── cd-dev.yml                # Development Environment Deployment
│       ├── cd-prod.yml               # Production Environment Deployment
│       └── monitoring.yml            # Monitoring Stack Deployment
├── src/
│   └── ...                          # Application Source Code
├── Dockerfile
├── helm/
│   └── my-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-staging.yaml
│       ├── values-prod.yaml
│       └── templates/
├── k8s/
│   ├── base/
│   └── overlays/
├── monitoring/
│   ├── alert-rules.yaml
│   ├── service-monitors.yaml
│   └── dashboards/
├── terraform/
│   └── ...                          # Infrastructure Code
└── README.md
```

---

## Summary

This tutorial provides a detailed introduction to the complete solution for integrating Kubernetes with GitHub Actions, from basic concepts to advanced practices, covering:

- **CI/CD Pipeline**: Automated workflow from code commit to production deployment
- **Deployment Strategies**: Multiple solutions including kubectl, Helm, Kustomize, ArgoCD, Flux CD
- **Multi-Environment Management**: Environment isolation and configuration management for dev/staging/prod
- **Autoscaling**: Elastic scaling solutions including HPA, VPA, KEDA
- **Monitoring and Alerting**: Prometheus + Grafana observability system
- **Security Practices**: RBAC, NetworkPolicy, image scanning and other security measures
- **Cloud Provider Integration**: Alibaba Cloud ACK, Tencent Cloud TKE, Huawei Cloud CCE
- **Cost Optimization**: Resource quotas, Spot instances, caching strategies
- **Domestic Practices**: Image acceleration, network optimization, compliance requirements

Through these practices, Chinese developers can build efficient, secure, and reliable cloud-native CI/CD pipelines.