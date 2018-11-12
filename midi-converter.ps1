$done = Get-ChildItem | Where-Object {$_.Extension -eq ".mxl"} | Select-Object -Property "BaseName" -Wait
$files = Get-ChildItem | Where-Object {($_.Extension -eq ".mid") -and ($_.Length -gt 2000) -and ($_.BaseName.Trim() -notin $done)}
for($i = 0; $i -lt $files.length; $i++)
{
    Write-Host "$($i+1) / $($files.length+1)"
    $name = $file.BaseName
    $process = Start-Process -FilePath "musescore" -Wait -ArgumentList "`"$file`" -o `"$name.mxl`"" -PassThru
    try
    {
        $process | Wait-Process -Timeout 15 -ErrorAction Stop
        Write-Warning -Message 'Process successfully completed within timeout.'
    }
    catch
    {
        Write-Warning -Message 'Process exceeded timeout, will be killed now.'
        $process | Stop-Process -Force
    }
}

