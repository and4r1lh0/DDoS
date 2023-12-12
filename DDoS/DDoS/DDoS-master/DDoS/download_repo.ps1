$url = "https://github.com/and4r1lh0/DDoS/archive/refs/heads/master.zip"
$output = "master.zip"
$start_time = Get-Date

# Import the BitsTransfer module if it is not already imported
if (!(Get-Module -Name BitsTransfer)) {
    Import-Module BitsTransfer
}

# Download the file asynchronously to improve performance
Start-BitsTransfer -Source $url -Destination ./master.zip
# Get the time taken to download the file
$download_time = (Get-Date).Subtract($start_time).Seconds

Write-Output "Time taken to download file: $download_time seconds"

# Extract the downloaded archive to the specified location
Expand-Archive -Path $output -DestinationPath "./DDoS" -Force