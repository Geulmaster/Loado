node (label: 'Win') {
    stage ('setup') {
        bat 'IF NOT EXIST "%CD%\Loado" git clone git@github.com:Geulmaster/Loado.git'
    }
    stage ('run sample') {
        steps: {
            bat "Loado\batch_files\get_basic.bat"
        }
    }
}