<#
Tim C Barnes
v0.3
2022-06-28

Loops through a destination directory.
For each item in the destination directory, choose to skip to the next item, exit the program, or continue.
Choosing to continue, enter the path to a relevant source directory in another location.
The contents of the two directories will be mergered into the destination.
Any duplicate items will be appended with "copy xx" where xx is an incremented number.
The original source directory is deleted and a shortcut to the desination directory is created in it's place. 
#>

$ErrorActionPreference = "Stop"

#Change these for different applications
$DestinationPath = "G:\My Drive\Lutron_Projects\HWQS"
$SourcePath = "G:\Shared drives\Captive_Shared\Projects"

:nextDirectory foreach ($Directory in Get-ChildItem $DestinationPath | Sort-Object)
{
    while($true)
    {
        Write-Host "`n`n$Directory is currently selected" -BackgroundColor Black
        $Selection = Read-Host -Prompt "Enter c to continue, s to skip, or x to exit"

        if (!$Selection)
        {
            Write-Host "`nPlease enter a selection!`n" -ForegroundColor Red -BackgroundColor Yellow
        }
        
        elseif ($Selection -eq "x")
        {
            break nextDirectory
        }

        elseif ($Selection -eq "s")
        {
            continue nextDirectory
        }

        elseif ($Selection -ne "c")
        {
            Write-Host "`nPlease enter a valid selection!`n" -ForegroundColor Red -BackgroundColor Yellow
        }

        else
        {

            while($true)
            {
                $ProjectName = Read-Host -Prompt "Enter the project directory, including parent (parent\target) or x to go back"
            
                # Bad things can happen if the script runs with empty arguments!
                if (!$ProjectName)
                {
                    Write-Host "`nPlease choose the project directory or x to exit!`n" -ForegroundColor Red -BackgroundColor Yellow
                }

                elseif ($ProjectName -eq "x")
                {
                    break
                }
            
                else
                {

                    $SourceTarget = "$SourcePath\$ProjectName"
                    $DestinationTarget = "$DestinationPath\$Directory"
                    
                    $DestinationFiles=Get-ChildItem $DestinationTarget
                    
                    Write-Host "`nMerging $SourceTarget with $DestinationTarget"
                    Get-ChildItem $SourceTarget | ForEach-Object {
                    
                        $counter=0
                        $name=$_.Name

                        while ($name -in $DestinationFiles.Name)
                        {
                            $counter++;
                            $name="{0} copy {1:d2}{2}" -f  $_.BaseName, $counter, $_.Extension
                        
                        }

                        Copy-Item -Path $_.FullName -Destination "$DestinationTarget\$name" 
                    
                    }

                    Write-Host "`nDeleting $SourceTarget directory"
                    Remove-Item -Recurse -Force $SourceTarget

                    Write-Host "Creating a new shortcut at $SourceTarget"
                    $WshShell = New-Object -comObject WScript.Shell
                    $Shortcut = $WshShell.CreateShortcut($SourceTarget + ".lnk")
                    $Shortcut.TargetPath = $DestinationTarget
                    $Shortcut.Save()
                    
                    Write-Host "`nAll operations completed successfully`n" -ForegroundColor Green -BackgroundColor Black
                    continue nextDirectory
                }
            }
        }
    }
}