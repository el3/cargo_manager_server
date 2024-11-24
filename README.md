Nuxt/Flask/NGINX boilerplate
============================

Useful to quickly get started on building Flask apps with modern frontend practices.

## Installation of development environment.

------------

1. Clone this repository: `git clone https://github.com/el3/cargo_manager_server && cd fluxt`
1. Install uwsgi: `pip install --user uwsgi`
1. Start the database server: `docker compose up -d db`
1. Create the backend virtualenv and activate it: `cd backend && python3 -mvenv env && source env/bin/activate`
1. Install backend runtime & test dependencies: `pip install -r requirements.txt -r requirements-test.txt`
1. Run database migrations: `flask db upgrade`
1. Run the development server: `cd .. && ./start_devserver.sh`
1. In a few seconds, the example chat app should be available at http://localhost:8080/ (if you're getting 502 Bad Gateway, be patient and try again :-) )

\

\

## Preparation of production server (using lighttpd as example)

------------

1. Install lighttpd, git, docker, and enable sshd.

2. Make a couple of folders:
   ```bash
   sudo mkdir /etc/lighttpd/conf-available && sudo mkdir /etc/lighttpd/conf-enabled && sudo mkdir /var/www/cargo_manager_server
   ```

3. Edit lighttpd config:
   ```bash
   sudo nano /etc/lighttpd/lighttpd.conf
   ```
   Add this line:
   ```plaintext
   include "conf-enabled/*.conf"
   ```

4. Make a new module:
   ```bash
   sudo nano /etc/lighttpd/conf-available/25-cargo_manager_server.conf
   ```
   Add the following configuration:
   ```plaintext
   server.modules += ( "mod_proxy" )

   $HTTP["url"] !~ "^/.well-known/" {
       proxy.server += ("" => ((
           "socket" => "/var/www/cargo_manager_server/proxy_run/nginx.sock"
       )))
   }
   ```

5. Create a symlink to the file in the conf-enabled directory:
   ```bash
   sudo ln -s /etc/lighttpd/conf-available/25-cargo_manager_server.conf /etc/lighttpd/conf-enabled/
   ```

6. Start lighttpd:
   ```bash
   sudo rc-update add lighttpd default && sudo rc-service lighttpd start
   ```

7. Create a bare git repository:
   ```bash
   git init --bare --initial-branch=cargo_manager cargo_manager_server
   ```
------------





## Push from the development environment to production server.

------------

### Dev environment

1. Go to your project folder on the dev environment. In this example:
   ```bash
   cd cargo_manager_server
   ```

2. Push to the bare repository:
   ```bash
   git push production_server_user@production_server_ip:cargo_manager_server cargo_manager
   ```
   - `cargo_manager` being the branch in this case.

### Production server

1. On the production server, perform a reset and clone operation:
   ```bash
   sudo rm -rf /tmp/temprepo && git clone ~/cargo_manager_server -b cargo_manager /tmp/temprepo
   ```

2. Go to the temprepo folder:
   ```bash
   cd /tmp/temprepo/
   ```

3. Copy a couple of files to the webapp folder:
   ```bash
   sudo cp docker-compose.yml /var/www/cargo_manager_server/
   sudo cp nginx.conf.template /var/www/cargo_manager_server/
   sudo cp .env /var/www/cargo_manager_server/
   ```

4. Build the images:
   ```bash
   docker compose build
   ```

5. Go to the webapp folder:
   ```bash
   cd /var/www/cargo_manager_server/
   ```

6. Change the permissions and ownership of the folder:
   ```bash
   sudo chown -R production_server_user: . && chmod 400 .env
   ```

7. Start the service:
   ```bash
   docker compose up --renew-anon-volumes --no-deps --detach
   ```

8. Upgrade the database in a temporary container:
   ```bash
   echo 'flask db upgrade' | docker compose run --rm backend sh
   ```

