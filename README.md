# Firebase leaked API-key checker
The tool checks configuration of firebase database.

### Disclaimer
Usage of tool for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

### Requirements
```
pip3 install loguru==0.6.0
pip3 install psutil==5.7.2
pip3 install aiohttp==3.9.0b0
pip3 install urllib3==2.2.1
pip3 install requests
pip3 install validators==0.18.2
pip3 install tldextract==2.2.3
pip3 install python-dateutil==2.8.2
```
### Arguments 
Runnig python
```
python3 firebase_api_key_checker.py [args...]
```
Checking one instance with printing requests and responses:
```
python3 firebase_api_key_checker.py -apikey "Firebase leaked key" -project "projectname"
python3 firebase_api_key_checker.py -apikey "Firebase leaked key" -project "projectname" -email "youremail@domain" -passwd "passwordforsignup"
```

|   Parameter   |  Description               | Value                                                            |
| ------------- | -------------------------- | ---------------------------------------------------------------- |
| -apikey       | Firebase leaked key        | "project_key@domain/path+id, project_key2@domain2/path2+id2"     |
| -project      | Firebase project name      | In pattern of: project_id.appspot.com, project_id.firebaseio.com |
| -email        | Custom email for signup    | Email address for registration, can be any                       |
| -passwd       | Custom password for signup | Password for registration, can be any                            |

### Docker 
If you do not want to install tool dependencies, then you can use the Docker image for testing. During development, I encountered a problem using urllib3, and therefore the Docker solution allows to test sites without installing conflicting versions.
Pull image to docker: 
```
docker pull olegbrain/firebase-checker
```
Run with arguments: 
```
docker run --rm -it olegbrain/firebase-checker  [args...]
```
