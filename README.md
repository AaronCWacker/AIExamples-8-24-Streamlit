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
Notice the path with ~AppData - this means that if username in Windows is aaron it would be installed in user's windows apps.  For me this path is the path to the 3.12.exe file to run py 3.12.5:  C:\Users\aaron\AppData\Local\Microsoft\WindowsApps
This also means that with a launch.json file used to debug that we will run python from there and also refer to our Scripts directory when examining install of requirements.txt libraries.
![image](https://github.com/user-attachments/assets/82d66224-5924-4537-8a5b-caebfdc18e12)

https://apps.microsoft.com/detail/9ncvdn91xzqp?hl=en-US&gl=US

# Install requirements.txt.

One thing you will notice is now MS has secured the python executables in a place where scripts and pip installs will be read only and thus they will install to your user directory:

PS C:\Users\aaron\Desktop\AIExamples\AIExamples-8-24-Streamlit> pip install -r requirements.txt
Defaulting to user installation because normal site-packages is not writeable

For my local debug install for latest VSCode this is in:
c:\users\aaron\appdata\local\packages\pythonsoftwarefoundation.python.3.12_qbz5n2kfra8p0\localcache\local-packages\python312\site-packages

This unique ID also matches this directory:
C:\Users\aaron\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0 which is where the launched version will reside.

Using the command line shell you will also notice that this scripts directory is not on your path.  Add it to your path to ensure that when executables from pypi packages for your user account are shelled from the correct location:

 WARNING: The script watchmedo.exe is installed in 'C:\Users\aaron\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location. 

If you navigate in Windows to Desktop then to your machine name, then open properties panel you can modify the path:

![image](https://github.com/user-attachments/assets/638eeaed-a5ab-469d-8ce9-53f6e6a5f627)

Add the two lines to your path at the top so performance from command line finds 3.12.5 easily along with any pip installed requirements.

![image](https://github.com/user-attachments/assets/102b0ff2-d703-43af-a1b3-b9029c670538)

After adding that and rerun of pip install -r requirements.txt you will see the warnings do not appear but launch.json still is unaware of where to find streamlit.exe

Assist by adding this same to your path inside launch.json.

.vscode/launch.json should now your path to streamlit:

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Streamlit: Run app.py",
            "type": "debugpy",
            "request": "launch",
            "program": "C:\Users\aaron\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\streamlit.exe",
            "args": [
                "run",
                "app.py"
            ],
            "console": "integratedTerminal"
        }
    ]
}





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
