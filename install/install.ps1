<#
  install.ps1 - 安装「神算子周半仙」算命 agent 团队

  用法：
    powershell -ExecutionPolicy Bypass -File install\install.ps1
    powershell -ExecutionPolicy Bypass -File install\install.ps1 -TargetDir "D:\my\agents"
    powershell -ExecutionPolicy Bypass -File install\install.ps1 -DatapackRoot "D:\datapack"
#>
param(
  [string]$TargetDir    = "$env:USERPROFILE\.zcode\agents",
  [string]$DatapackRoot = ""
)

$ErrorActionPreference = "Stop"
$here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo   = Split-Path -Parent $here
$srcDir = Join-Path $repo "agents"

Write-Host ""
Write-Host "=== 算命 agent 团队 安装程序 ===" -ForegroundColor Cyan
Write-Host "源目录  : $srcDir"
Write-Host "目标目录: $TargetDir"
if ($DatapackRoot) { Write-Host "数据包  : $DatapackRoot" } else { Write-Host "数据包  : 未指定（agent 将走降级路径，功能不受影响）" }
Write-Host ""

if (-not (Test-Path $srcDir)) { Write-Host "错误：找不到 agents 目录：$srcDir" -ForegroundColor Red; exit 1 }
New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

$marker = '{{DATAPACK_ROOT}}'
$replace = if ($DatapackRoot) { $DatapackRoot.TrimEnd('\') } else { 'NOT_INSTALLED' }
$installed = @()

Get-ChildItem (Join-Path $srcDir "*.md") | ForEach-Object {
  $text = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
  $text = $text.Replace($marker, $replace)
  $dest = Join-Path $TargetDir $_.Name
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($dest, $text, $utf8NoBom)
  $installed += $_.Name
  Write-Host ("  [OK] {0,-30} {1,7} bytes" -f $_.Name, (Get-Item $dest).Length)
}

Write-Host ""
Write-Host "已安装 $($installed.Count) 个 agent 到：" -ForegroundColor Green
Write-Host "  $TargetDir"
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "  1) 重启宿主，使新 agent 被加载"
Write-Host "  2) 在 agent 列表选择「神算子周半仙」开始提问"
Write-Host "  3) 按 docs\VERIFY.md 做验收（尤其 V4 分诊与 V5 断网自包含性）"
Write-Host ""
Write-Host "自检：确认没有留下源码机的绝对路径 ->"
$leak = Select-String -Path (Join-Path $TargetDir "*.md") -Pattern 'D:\\', 'Obsidian', '/home/', '/Users/' -ErrorAction SilentlyContinue
if ($leak) { Write-Host "  [警告] 发现残留绝对路径，agent 可能读取失败：" -ForegroundColor Red; $leak | Select-Object -First 5 | ForEach-Object { Write-Host "    $($_.Line.Trim())" } }
else       { Write-Host "  [通过] 无绝对路径残留" -ForegroundColor Green }
Write-Host ""
