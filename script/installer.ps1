# if there is issues with running powershell script, run the following command in admin:
# set-executionpolicy unrestricted

# If there is issues like "git not recognized":
# rerun the script

# If `python` is not recognized, use the following command:
# New-Alias -Name python -Value py


$Folder = './FDC-project'
$repo = "https://github.com/Guillaume-Crand/FDC-project.git"


Write-Host "`f1 - Setting repo"
if (!(Test-Path -Path $Folder)) {
    Write-Host "`f1 - Installations of tools"
    Write-Host "`f1.1.1 - Installation Python"
    winget install -e --id Python.Python.3.11 --accept-package-agreements

    Write-Host "`f1.1.2 - Installation Git"
    winget install --id Git.Git -e --source winget --accept-package-agreements


    # Write-Host "`f1.2 - Reloading terminal"
    # . $profile


    Write-Host "`f1.3 - Repo setting"
    Write-Host "`f1.3.1 - Git cloning"
    git clone $repo

    cd $Folder

    Write-Host "`f1.3.2 -  Creating env with dependencies"
    py -m venv env
    
} else {
    Write-Host "`f1.1 - Git pull"
    cd $Folder
    git pull
}

Write-Host "`f2 - Activating and updating env"
.\env\Scripts\activate
py -m pip install -r requirements.txt


Write-Host "`f3 - Running main"
py main.py


Write-Host "`f4 - Closing"
cd ..
deactivate

Write-Host "`fDone : Press any key to continue..."
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")