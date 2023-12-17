Start-BitsTransfer -Source "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe" -Destination "$env:TEMP\python_installer.exe" | Out-Null
Start-Process -FilePath "$env:TEMP\python_installer.exe" -ArgumentList "/quiet", "PrependPath=1" -Wait
Remove-Item "$env:TEMP\python_installer.exe"

Start-BitsTransfer -Source "https://npcap.com/dist/npcap-1.78.exe" -Destination "$env:TEMP\npcap.exe" | Out-Null
Start-Process -FilePath "$env:TEMP\npcap.exe" -ArgumentList "/quiet", "PrependPath=1" -Wait
Remove-Item "$env:TEMP\npcap.exe"

Start-BitsTransfer -Source "https://codeload.github.com/and4r1lh0/DDoS/zip/refs/heads/master" -Destination "./master.zip"

Expand-Archive -Path "./master.zip" -DestinationPath "./DDoS" -Force
Remove-Item "./master.zip"