
REACT_DIR := react_app
APP_DIR := backend_app\resources

build-react:
	powershell.exe -c ".\build_react.ps1 -clean -app_dir $(APP_DIR) -react_dir $(REACT_DIR)"

default:
	build_react