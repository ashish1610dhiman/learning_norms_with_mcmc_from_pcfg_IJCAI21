# From willy denoyette: https://answers.microsoft.com/en-us/insider/forum/insider_wintp-insider_web-insiderplat_pc/timethisexe/e7163d08-e616-4408-95f9-df78d13ed52f
# May first need to run "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"
param([string]$command)
$x = Invoke-Expression -Command $command
measure-command {$x | write-host}