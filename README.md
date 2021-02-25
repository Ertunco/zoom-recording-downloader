## Create a JWT Token
### Create a JWT App
JSON Web Token (JWT) offer a method to generate tokens that provide secure data transmission using a neat and compact JSON object.
JWTs contain signed payload that helps establish server to server authentication.
If your app is meant to be used only by yourself or by users that are in your Zoom account, it is recommended that you use JWT for authentication.
To do this, register a  in the Zoom App Marketplace.

### Register your App
Login using your username and password to [https://marketplace.zoom.us/](https://marketplace.zoom.us/)
Click on the Develop option in the dropdown on the top-right corner and select Build App.
A page with various app types will be displayed.
Select JWT as the app type and click on Create.

## Setup
Clone the repository to your local computer
```
git clone https://github.com/Ertunco/zoom-recording-downloader.git
```

Create a virtual environment (built-in venv module) using the below command on your project folder so it should look like below;
```
python -m venv your_env_name
```

Activate the virtual environment using below command.
```
source your_env_name/bin/activate
```

If you need to deactivate your environment you can use the command below but this is not the case for this project;
```
deactivate
```

Install the packages using requirements.txt file on the virtual environment.
```
pip install -r requirements.txt
```

## Execution
```
python zoom_recording_downloader.py
```



