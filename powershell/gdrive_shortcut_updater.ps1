<#
Tim C Barnes
v0.0.1
2022-09-14

Iterates through a directory looking for "Lighting.lnk" files and updating their
target paths to the new location.
Pulls the useful part of the current .lnk target path out,
add the useful part to the new path and saves it.
#>

$ProjectsPath = "G:\Shared drives\Captive_Shared\Projects\"
$TargetPath = "G:\.shortcut-targets-by-id\0B9nhPAEMRdI4flJMVEFzSmpaMERNTVFzbEU2cVN3WlV5MkgzaHBPYmVULVlsZkVSR2xpTFk\"

:nextDirectory foreach ($Directory in Get-ChildItem $ProjectsPath | Sort-Object)
{
    $ShortcutToChange = Get-ChildItem -Path $Directory -Filter "Lighting.lnk"
    if($ShortcutToChange -like "*Lighting.lnk*")
    {
        $WshShell = New-Object -comObject WScript.Shell

        # Get the current target path of the shortcut
        $OldTarget = $WshShell.CreateShortcut($ShortcutToChange.FullName).TargetPath

        # Pull out the part of the path that starts with Lutron_Projects
        $OldTarget = $OldTarget.Substring($OldTarget.IndexOf("Lutron_Projects"))

        # Add the new path and old path together
        $NewTarget = $TargetPath + $OldTarget

        # Get the shortcut object, overwrite it's target path, and save it.
        $Shortcut = $WshShell.CreateShortcut($ShortcutToChange.FullName)
        $Shortcut.TargetPath = $NewTarget
        $Shortcut.Save()

    } else {

        continue nextDirectory

    }
}

Write-Host "All Shortcuts updated"