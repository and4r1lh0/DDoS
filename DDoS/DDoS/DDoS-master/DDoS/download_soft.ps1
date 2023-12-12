$pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$pythonInstaller = "$env:TEMP\python_installer.exe"

$webClient = New-Object System.Net.WebClient
$webClient.DownloadFileAsync($pythonUrl, $pythonInstaller) | Out-Null

while ($webClient.IsBusy) {
    Start-Sleep -Milliseconds 500
}



Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "PrependPath=1" -Wait
Remove-Item $pythonInstaller

$url = "https://www.win10pcap.org/download/Win10Pcap-v10.2-5002.msi"
$filePath = "$env:TEMP\win10pcap.msi"

$webClient = New-Object System.Net.WebClient
$webClient.DownloadFileAsync($url, $filePath) | Out-Null

while ($webClient.IsBusy) {
    Start-Sleep -Milliseconds 500
}

Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $filePath /passive" -Wait
Remove-Item $filePath