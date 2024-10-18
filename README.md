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
3. Use uv to run manage.py commands (start the dev server)

  ```shell
  uv run manage.py runserver 0.0.0.0:8000
  ```
