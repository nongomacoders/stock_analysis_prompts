$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$taskTempRoot = [IO.Path]::GetFullPath((Join-Path $taskRoot 'tmp'))
$taskNames = @(
  'logical-capture-targeted-20261028',
  'logical-capture-integration-20261028',
  'logical-capture-repair-20261028',
  'logical-capture-full-20261028',
  'logical-capture-final-20261028',
  'logical-capture-shared-page-20261028',
  'logical-capture-verified-20261028'
)
$taskTargets = @()
foreach ($taskName in $taskNames) {
  $taskTarget = [IO.Path]::GetFullPath((Join-Path $taskTempRoot $taskName))
  if (-not $taskTarget.StartsWith($taskTempRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Cleanup target outside the task's tmp directory."
  }
  $taskTargets += $taskTarget
}
$taskDeleted = @()
foreach ($taskTarget in $taskTargets) {
  if (Test-Path -LiteralPath $taskTarget) {
    Remove-Item -LiteralPath $taskTarget -Recurse -Force
    $taskDeleted += $taskTarget
  }
}
@{deleted=$taskDeleted;remaining=@($taskTargets | Where-Object {Test-Path -LiteralPath $_})} | ConvertTo-Json -Compress
