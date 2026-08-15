$ErrorActionPreference='Stop'
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $root
$ip=(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notmatch '^127\.' -and $_.PrefixOrigin -ne 'WellKnown'} | Select-Object -First 1 -ExpandProperty IPAddress)
Write-Host "Accueil local : http://127.0.0.1:8894/"
Write-Host "Téléphone/PC : http://${ip}:8894/"
python -m http.server 8894 --bind 0.0.0.0
