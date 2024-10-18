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
3. Use [uv](https://docs.astral.sh/uv/getting-started/installation/) to run manage.py commands (create the database)

  ```shell
  uv run manage.py migrate
  ```

4. Start the dev server

  ```shell
  uv run manage.py runserver 0.0.0.0:8000
  ```
