# AIExamples-8-24-Streamlit
AIExamples-8-24-Streamlit

# VSCode Extensions
1. Azure Resources
2. Azure Account
3. Azure App Services
4. Azure CLI Tools
5. Azure Functions
6. Azure Resource Manager Snippets
7. Azure Resource Manager Tools

# Use Latest VSCode Insiders - 1.93 system

![image](https://github.com/user-attachments/assets/096fbb1f-1075-4b12-83ca-96861260ce8e)

# Use Latest Python - 3.12.5 using In VSCode Ctrl-Shift-P for Select: Python Interpreter
If using torch use 3.11 as 3.12 is not supported yet.

![image](https://github.com/user-attachments/assets/82d66224-5924-4537-8a5b-caebfdc18e12)

https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=en-US&gl=US






# Deploy as Web App on AZ:

## Startup Command:
Python 3.11
pip3 install -r requirements.txt  |  python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0

## Platform settings:
SCM off
FTP off
SSH on
Always On on
HTTPS only on
Remote debug off
Cert ignore

## Custom domains
20.119.8.32 ip
Custom domains:  ai-01.azurewebsites.net

## Network
Inbound traffic config
Public: Enabled no restrict
Inbound address




# Detailed VNET for ACA

```mermaid
graph LR
    subgraph VNET["VNET"]
        subgraph ContainerAppEnv["Container App Environment Subnet"]
            ACA1["ACA-app1"]
            ACA2["ACA-app2"]
            Envoy["Envoy"]
            ILB[("ILB\nPrivate IP")]
            ACA1 --> |FQDN| Envoy
            ACA2 --> |FQDN| Envoy
            Envoy --> ILB
        end
        subgraph AppGatewaySubnet["App Gateway Subnet"]
            AppGateway["App Gateway"]
            BackendSettings["backend settings\nFQDN (ACA-app1)"]
        end
        ILB -.-> |traffic| AppGateway
    end
    PublicIP[("Public IP")] --> AppGateway
    User["User"] --> |https://mycompany.com| PublicIP
    
    subgraph PrivateDNSZone["Private DNS Zone"]
        DNS{{"FQDN(ACA-app1)\nILB-IP"}}
    end
    DNS -.-> ContainerAppEnv

    KeyVault["Key vault"] --> |TLS cert| AppGateway
    AppGateway --> |MI| KeyVault

    AppServiceDomain["App Service Domain"] --> AzureDNSZone["Azure DNS Zone"]

    subgraph Notes["Container Apps Env"]
        Note1["internal mode"]
        Note2["No default DNS resolution"]
        Note3["No public endpoint"]
        Note4["static IP = ILB-IP"]
    end

    classDef subnet fill:#e6f3ff,stroke:#6ca9e6;
    class ContainerAppEnv,AppGatewaySubnet subnet;
    
    classDef vnet fill:#c1e3ff,stroke:#4a90e2;
    class VNET vnet;
    
    classDef publicIP fill:#ffcccb,stroke:#ff6b6b;
    class PublicIP publicIP;
    
    classDef dnsZone fill:#fff2cc,stroke:#ffcd28;
    class PrivateDNSZone,AzureDNSZone dnsZone;

    classDef notes fill:#f9f9f9,stroke:#d9d9d9;
    class Notes notes;

```





# Simple VNET for ACA
```mermaid
graph LR
    subgraph VNET["VNET"]
        subgraph ContainerAppEnv["Container App Environment Subnet"]
            ACA1[ACA-app1]
            ACA2[ACA-app2]
            Envoy
            ILB[("ILB\nPrivate IP")]
            ACA1 --> |FQDN| Envoy
            ACA2 --> |FQDN| Envoy
            Envoy --> ILB
        end
        subgraph AppGatewaySubnet["App Gateway Subnet"]
            AppGateway["App Gateway"]
        end
        ILB -.-> |traffic| AppGateway
    end
    PublicIP[("Public IP")] --> AppGateway
    
    subgraph PrivateDNSZone["Private DNS Zone"]
        DNS{{"FQDN(ACA-app1)\nILB-IP"}}
    end
    DNS -.-> ContainerAppEnv

    classDef subnet fill:#e6f3ff,stroke:#6ca9e6;
    class ContainerAppEnv,AppGatewaySubnet subnet;
    
    classDef vnet fill:#c1e3ff,stroke:#4a90e2;
    class VNET vnet;
    
    classDef publicIP fill:#ffcccb,stroke:#ff6b6b;
    class PublicIP publicIP;
    
    classDef dnsZone fill:#fff2cc,stroke:#ffcd28;
    class PrivateDNSZone dnsZone;
```
