$types = "test","train"
$composers = "schubert"
#$composers = dir -Directory | where -na
Foreach($composer in $composers)
{
    cd $composer
    Foreach($type in $types)
    {
        cd $type
        $done = Get-ChildItem | Where-Object {$_.Extension -eq ".mxl"} | Select-Object -ExpandProperty "BaseName" 
        $files = Get-ChildItem | Where-Object {($_.Extension -eq ".mid") -and ($_.BaseName -notin $done)}
        for($i = 0; $i -lt $files.length; $i++)
        {
            $file = $files[$i]
            Write-Progress -Activity "Converting to mxl" -PercentComplete $(($i / $files.length) * 100) -Status "File $($i+1)/$($files.length) $composer/$type/$file"
            $name = $file.BaseName
            $process = Start-Process -FilePath "musescore" -Wait -ArgumentList "`"$file`" -o `"$name.mxl`"" -PassThru
            try
            {
                $process | Wait-Process -Timeout 15 -ErrorAction Stop
            }
            catch
            {
                Write-Warning -Message 'Process exceeded timeout, will be killed now.'
                $process | Stop-Process -Force
            }
        }
        cd ..
    }
    cd ..
}
