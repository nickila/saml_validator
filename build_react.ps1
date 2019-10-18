param (
    [string]$app_dir = "backend_app\resources",
    [string]$react_dir = "react_app",
    [Switch]$clean
)


$build_dir = "$react_dir\build"
$meta_dir = "$app_dir\static\meta"
$templates_dir = "$app_dir\templates"

Remove-Item -Recurse -Force $build_dir -ErrorAction SilentlyContinue
Set-Location $react_dir

try
{
    npm run build
}
finally
{
    Set-Location ..
}

if ($clean.IsPresent)
{
    Remove-Item -Recurse -Force "$app_dir\static" -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force "$app_dir\templates" -ErrorAction SilentlyContinue
}

Copy-Item "$build_dir\static" "$app_dir" -Recurse -Force
New-Item -Path "$templates_dir"-ItemType Directory -Force | Out-Null
New-Item -Path "$meta_dir"-ItemType Directory -Force | Out-Null


Copy-Item -Path (Get-Item -Path "$build_dir\*" -Exclude 'static') -Destination "$meta_dir" -Force
Move-Item -Path "$meta_dir\*.html" -Destination "$templates_dir" -Force

