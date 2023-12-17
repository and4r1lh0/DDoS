$webClient = New-Object System.Net.WebClient
$webClient.DownloadFileAsync("https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe", "$env:TEMP\python_installer.exe") | Out-Null

while ($webClient.IsBusy) {
    Start-Sleep -Milliseconds 500
}

Start-Process -FilePath "$env:TEMP\python_installer.exe" -ArgumentList "/quiet", "PrependPath=1" -Wait
Remove-Item "$env:TEMP\python_installer.exe"


$webClient = New-Object System.Net.WebClient
$webClient.DownloadFileAsync("https://www.win10pcap.org/download/Win10Pcap-v10.2-5002.msi", "$env:TEMP\win10pcap.msi") | Out-Null

while ($webClient.IsBusy) {
    Start-Sleep -Milliseconds 500
}

Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $env:TEMP\win10pcap.msi /passive" -Wait
Remove-Item "$env:TEMP\win10pcap.msi"


# Import the BitsTransfer module if it is not already imported
if (!(Get-Module -Name BitsTransfer)) {
    Import-Module BitsTransfer
}

# Download the file asynchronously to improve performance
Start-BitsTransfer -Source "https://github.com/and4r1lh0/DDoS/archive/refs/heads/master.zip" -Destination "./master.zip"

# Extract the downloaded archive to the specified location
Expand-Archive -Path "./master.zip" -DestinationPath "./DDoS" -Force
Remove-Item "./master.zip"