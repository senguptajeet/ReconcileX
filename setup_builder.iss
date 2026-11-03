[Setup]
; Application Information
AppName=ReconcileX
AppVersion=1.0
AppPublisher=ReconcileX
DefaultDirName={autopf}\ReconcileX
DefaultGroupName=ReconcileX

; Installer Output Configuration
OutputDir=installer_build
OutputBaseFilename=ReconcileX_Windows_Setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=lowest

; Custom Installer Icon
SetupIconFile=assets\app_icon.ico

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; IMPORTANT: This points to the folder PyInstaller just created
Source: "dist\ReconcileX\ReconcileX.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ReconcileX\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ReconcileX"; Filename: "{app}\ReconcileX.exe"
Name: "{autodesktop}\ReconcileX"; Filename: "{app}\ReconcileX.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\ReconcileX.exe"; Description: "{cm:LaunchProgram,ReconcileX}"; Flags: nowait postinstall skipifsilent