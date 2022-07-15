<#
Tim Barnes
v1.0
2022-07-15

Fetches specific NVX firmware versions from Crestron's ftp servers.
Pushes the specified firmware to NVX endpoints on the network.
#>

Import-Module PSCrestron

$user = ""
$pass = ""
$fgetusr = ""
$fgetpass = ""
$fw30 = "dm-nvx_3.0.4472.00077.puf "
$fw41 = "dm-nvx_4.1.4472.00021.puf"
$fw52 = "dm-nvx-ed30-enc_5.2.4651.00018_r400406.zip"
$fw60 = "dm-nvx-ed30-enc_6.0.4835.00027_r416525.zip"

#Update to nvx_3.0
$cmd1 = "FGET  ftp://ftp.crestron.com/firmware/dm-nvx/${fw30} /firmware/${fw30} ${fgetusr}:${fgetpass}"

#Update to nvx_4.1
$cmd2 = "FGET  ftp://ftp.crestron.com/firmware/dm-nvx/${fw41} /firmware/${fw41} ${fgetusr}:${fgetpass}"

#update to nvx_5.2
$cmd3 = "FGET  ftp://ftp.crestron.com/firmware/dm-nvx/${fw52} /firmware/${fw52} ${fgetusr}:${fgetpass}"

#update to nvx_6.0
$cmd4 = "FGET  ftp://ftp.crestron.com/firmware/dm-nvx/${fw60} /firmware/${fw60} ${fgetusr}:${fgetpass}"

$ipa = @(
'192.168.5.71'
'192.168.5.72'
'192.168.5.73'
'192.168.5.74'
'192.168.5.75'
'192.168.5.76'
'192.168.5.77'
'192.168.5.91'
'192.168.5.92'
'192.168.5.93'
'192.168.5.94'
'192.168.5.95'
'192.168.5.96'
)

if(!$args) {
    write-host "`nUsage:`n-v check firmware version`n-f check firmware directory contents`n-d 3.0, 4.1, 5.2, 6.0 download corresponding firmware version`n-z update firmware with .zip format`n-p update firmware with .puf format"

} elseif($args[0] -eq "-v") {
    write-host "Checking firmware version"
    
    ForEach($ipaddr in $ipa) {
        Invoke-CrestronCommand -Device $ipaddr -Command "VER" -Secure -Username $user -Password $pass
    }

} elseif($args[0] -eq "-f") {
    write-host "Checking firmware directory"
    
    ForEach($ipaddr in $ipa) {
        Invoke-CrestronCommand -Device $ipaddr -Command "dir /firmware" -Secure -Username $user -Password $pass
    }

} elseif($args[0] -eq "-d") {
    if(!$args[1]) {
        write-host "Firmware version required"
    
    }elseif($args[1] -eq "3.0") {
        write-host "Downloading firmware version ${fw30}"
        
        ForEach($ipaddr in $ipa) {
            Invoke-CrestronCommand -Device $ipaddr -Command $cmd1 -Secure -Username $user -Password $pass
        }
    
    } elseif($args[1] -eq "4.1") {
        write-host "Downloading firmware version ${fw41}"
        
        ForEach($ipaddr in $ipa) {
            Invoke-CrestronCommand -Device $ipaddr -Command $cmd2 -Secure -Username $user -Password $pass
        }
    
    } elseif($args[1] -eq "5.2") {
        write-host "Downloading firmware version ${fw52}"
        
        ForEach($ipaddr in $ipa) {
            Invoke-CrestronCommand -Device $ipaddr -Command $cmd3 -Secure -Username $user -Password $pass
        }
    
    } elseif($args[1] -eq "6.0") {
        write-host "Downloading firmware version ${fw60}"
        
        ForEach($ipaddr in $ipa) {
            Invoke-CrestronCommand -Device $ipaddr -Command $cmd4 -Secure -Username $user -Password $pass
        }
    
    } else {
        write-host "Invalid firmware version"
        write-host "Valid versions: 3.0, 4.1, 5.2, 6.0"
    }

} elseif($args[0] -eq "-z") {
    write-host "Updating firmware with .zip image"
    
    ForEach($ipaddr in $ipa) {
        Invoke-CrestronCommand -Device $ipaddr -Command "IMGUPD" -Secure -Username $user -Password $pass
    }

} elseif($args[0] -eq "-p") {
    write-host "Updating firmware with .puf image"
    
    ForEach($ipaddr in $ipa) {
        Invoke-CrestronCommand -Device $ipaddr -Command "PUF" -Secure -Username $user -Password $pass
    }

} else {
    write-host "Invalid parameter"
    write-host "`nUsage:`n-v check firmware version`n-f check firmware directory contents`n-d 3.0, 4.1, 5.2, 6.0 download corresponding firmware version`n-z update firmware with .zip format`n-p update firmware with .puf format"
}