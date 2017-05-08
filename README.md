# keyformproject
## Setting up the development environment on Linux
1. Clone into the Git repository

  ```shell
  git clone https://github.com/mostateresnet/keyformproject.git
  ```
2. Switch to the newly created `keyformproject` directory

  ```shell
  cd keyformproject
  ```
3. Create a new virtual environment for keyformproject

  ```shell
  mkvirtualenv --python=$(which python3) keyformproject
  ```
4. Install the required Python packages

  ```shell
  pip install -U pip -r requirements/development.txt
  ```
5. Re-activate the Python virtual environment to ensure all the environment variables are reset to their proper values

  ```shell
  workon keyformproject
  ```

## Testing
To test using your browser of choice pass the -b option to manage.py test (phantomjs is the default):
```shell
python manage.py test -b chrome
``` 

If you would like to test using an android device you will need to setup the Remote webdriver for android then you can specify the broadcast address for the test server:
```shell
python manage.py test -b remote --liveserver=0.0.0.0:8081
```
The test runner will automatically try to acertain and test using the hostname of the machine running the tests if the ip is 0.0.0.0
