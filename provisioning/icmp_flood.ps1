Start-BitsTransfer -Source "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe" -Destination "$env:TEMP\python_installer.exe"
Start-Process -FilePath "$env:TEMP\python_installer.exe" -ArgumentList "/quiet", "PrependPath=1" -Wait

Start-BitsTransfer -Source "https://npcap.com/dist/npcap-1.78.exe" -Destination "$env:TEMP\npcap.exe"
Start-Process -FilePath "$env:TEMP\npcap.exe" -ArgumentList "/quiet", "PrependPath=1" -Wait

Start-BitsTransfer -Source "https://raw.githubusercontent.com/and4r1lh0/DDoS/master/provisioning/ICMP-Flood.zip" -Destination "./ICMP-Flood.zip"
Expand-Archive -Path "./ICMP-Flood.zip" -Force

Remove-Item "$env:TEMP\python_installer.exe"
Remove-Item "$env:TEMP\npcap.exe"
Remove-Item "./ICMP-Flood.zip"