# GitHub + Azure DevOps Integration

## Why Integrate Azure DevOps?

Azure DevOps is Microsoft's enterprise-level DevOps platform, deeply integrated with GitHub, providing complete ALM (Application Lifecycle Management).

## Integration Methods

| Method | Description |
|--------|-------------|
| Azure Pipelines | Directly use Azure DevOps for build and deploy |
| GitHub Actions | Use Azure tasks in GitHub |
| Boards Integration | Azure Boards associates with GitHub Issues |
| Artifacts | Package management integrates with GitHub Packages |
| Test Plans | Test management associates with PRs |

## Azure Pipelines + GitHub

### Basic Configuration

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'

steps:
- task: UseNode@1
  inputs:
    version: '20'

- script: |
    npm ci
    npm run build
    npm test
  displayName: 'Build and Test'

- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'test-results.xml'
```

### Deploy to Azure

```yaml
# Deploy to Azure App Service
- task: AzureWebApp@1
  inputs:
    azureSubscription: 'Azure-Connection'
    appType: 'webApp'
    appName: 'my-app'
    package: '$(Build.ArtifactStagingDirectory)/**/*.zip'
```

### Deploy to Azure Container Instances

```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: 'Azure-Connection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      az container create \
        --resource-group myRG \
        --name myContainer \
        --image myregistry.azurecr.io/myapp:$(Build.BuildId) \
        --dns-name-label myapp \
        --ports 80
```

## GitHub Actions for Azure

### Login to Azure

```yaml
# .github/workflows/azure-deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'my-app'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: './dist'
```

### Using Azure CLI

```yaml
- name: Azure CLI Action
  uses: azure/cli@v1
  with:
    inlineScript: |
      az webapp deployment source config \
        --name my-app \
        --resource-group myRG \
        --repo-url ${{ github.repository }} \
        --branch main \
        --manual-integration
```

### Create Azure Resources

```yaml
- name: Create Azure Resource Group
  uses: azure/cli@v1
  with:
    inlineScript: |
      az group create --name myRG --location eastasia

- name: Create Azure Container Registry
  uses: azure/cli@v1
  with:
    inlineScript: |
      az acr create \
        --resource-group myRG \
        --name myregistry \
        --sku Basic
```

## Azure Boards + GitHub

### Associate Issues

```bash
# Associate GitHub Issues in Azure Boards
# 1. Enable GitHub integration in Azure Boards settings
# 2. Select GitHub repository to associate
# 3. Use #ID in Issues to associate work items
```

### Automatic Association

```yaml
# Use special syntax in GitHub Issues
# AB#123 - Associate Azure Boards work item
# Fixes AB#123 - Associate and auto-close
```

## Azure Artifacts + GitHub

### Publish to Azure Artifacts

```yaml
- task: Npm@1
  inputs:
    command: 'publish'
    publishRegistry: 'useFeed'
    publishFeed: 'my-feed'
    workingDir: '.'
    verbose: true
```

### Migrate from GitHub Packages

```bash
# Use Azure Artifacts
npm config set registry https://pkgs.dev.azure.com/myorg/_packaging/myfeed/npm/registry/

# Publish package
npm publish
```

## Azure DevOps GitHub App

### Installation

1. Visit https://github.com/marketplace/azure-devops
2. Click Install
3. Select repositories
4. Authorize access

### Features

| Feature | Description |
|---------|-------------|
| Work Item Association | PR associates with Azure Boards |
| Status Check | Build status updates to PR |
| Deployment Tracking | Deployment status displayed in GitHub |
| Security Scan | Code security check |

## Best Practices

1. **Unified Identity**: Use Azure AD with GitHub same account
2. **Environment Separation**: Separate Staging and Production
3. **Secure Storage**: Use Azure Key Vault for key management
4. **Monitoring Alerts**: Use Azure Monitor to monitor applications
5. **Cost Optimization**: Use Azure Cost Management

## Related Resources

- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/)
- [GitHub Actions for Azure](https://github.com/Azure/actions)
- [Azure GitHub Integration](https://docs.microsoft.com/en-us/azure/developer/github/)
