<#
Tim C Barnes
v1.0
2022-06-24

Moves a directory from one hardcoded location to another.
Deletes an existing windows shortcut to the directory.
The directory is renamed in the process and a new windows shortcut to it is left in the original location.
The user is prompted for the exact name of the parent directory and the exact name of the existing shortcut.
The user can continue performing these operations consecutively after responding to a continuation prompt.
The current hardcoded paths leverage the Google Drive desktop file structure.
#>

$ErrorActionPreference = "Stop"

do
{
    while($true)
    {
        $ProjectName = Read-Host -Prompt "Enter the parent directory of the source"
        #$LutronName = Read-Host -Prompt "Enter the destination directory"
    
        # Bad things can happen if the script runs with empty arguments!
        if ((!$ProjectName) <#-or (!$LutronName)#>)
        {
            Write-Host "`nPlease define all arguments!`n" -ForegroundColor Red -BackgroundColor Yellow
        }
    
        else
        {
            Break
        }
    }

    #Edit these for different directory locations
    $LutronVersion = "HWQSX"
    $SourcePath = "G:\Shared drives\Captive_Shared\Projects"
    $DestinationPath = "G:\My Drive\Lutron_Projects"

    $SourceTarget = "$SourcePath\$ProjectName\Lighting"
    $DestinationTarget = "$DestinationPath\$LutronVersion\$ProjectName"
    #$LutronFolder = "$DestinationPath\$LutronVersion\$LutronName"

    #Write-Host "`nDeleting the old $LutronName shortcut"
    #rm "$($LutronFolder)*.lnk"

    Write-Host "`nMoving the 'Lighting' directory in $SourcePath\$ProjectName to $DestinationTarget"
    Move-Item -Path $SourceTarget -Destination $DestinationTarget
    
    Write-Host "Creating a new shortcut at $SourceTarget"
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($SourceTarget + ".lnk")
    $Shortcut.TargetPath = $DestinationTarget
    $Shortcut.Save()
    
    Write-Host "`nAll operations completed successfully`n" -ForegroundColor Green -BackgroundColor Black

    $Continue = Read-Host -Prompt "Enter any key to process another request, or X to exit"
}

until ($Continue -like 'x')