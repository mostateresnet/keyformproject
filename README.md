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
  
