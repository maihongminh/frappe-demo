### Hướng dẫn cài đặt Frappe Education (môi trường phát triển trên Windows + WSL)

Tài liệu này hướng dẫn từng bước, kèm giải thích bằng tiếng Việt cho mỗi lệnh, để bạn thiết lập môi trường phát triển local cho ứng dụng `education` (Frappe/ERPNext v15 + frontend Vite).

---

## 1) Chuẩn bị môi trường (khuyến nghị dùng WSL + Ubuntu)

- Cài WSL và Ubuntu (chạy ở PowerShell với quyền Administrator):

```powershell
wsl --install -d Ubuntu
```
- Giải thích: Cài đặt Windows Subsystem for Linux cùng bản phân phối Ubuntu, giúp chạy môi trường Linux phù hợp cho Frappe.

* Nên cài đặt Ubuntu trực tiếp từ microsorft : 
https://apps.microsoft.com/detail/9pn20msr04dw?hl=vi-VN&gl=VN

Sau khi cài xong, khởi động lại máy, mở Ubuntu, tạo user và cập nhật hệ thống:

```bash
sudo apt update && sudo apt upgrade -y
```
- Giải thích: Cập nhật danh sách gói (`apt update`) và nâng cấp các gói đang cài (`apt upgrade`).

## 2. Cài git, python, and redis

```bash
sudo apt install git python-is-python3 python3-dev python3-pip redis-server libmariadb-dev mariadb-server mariadb-client pkg-config

```
## 3. Cài MariaDB và thiết lập cơ bản:
```bash
sudo mariadb-secure-installation
```

```bash
sudo mysql -u root
```
Trong MySQL shell, chạy:

```sql
SET GLOBAL innodb_file_per_table=1;
SET GLOBAL character_set_server = 'utf8mb4';
SET GLOBAL collation_server = 'utf8mb4_unicode_ci';
```
- Giải thích: Bật tách file cho mỗi bảng InnoDB và đặt charset/collation mặc định sang `utf8mb4` phù hợp Unicode.

Thoát MySQL shell:

```sql
\q
```
- Giải thích: Lệnh `\q` (hoặc `exit`, `quit`, Ctrl+D) để thoát trình khách MySQL.

tiến hành khởi động lại dịch vụ MariaDB
``` bash
sudo systemctl restart mariadb
```

## 4. Cài đặt nvm

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```
-Lưu ý: sau khi cài xong thì tiến hành cài nvm bash_completion 
chạy lại đoạn export ở cuối log sau khi cài đặt node.js

export sẽ có định dạng tương tự:
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

## 5. cài đặt node

``` bash
nvm install 22 # or 20, 18,24 

```
-kiểm tra version để xem thử đã cài đặt thành công hay chưa :
```bash
node -v
```
## 6. cài đặt yarn bằng cách sử dụng npm
``` bash
npm install -g yarn

```

## 7. Cài đặt gói wkhtmltopdf
```bash
sudo apt-get update
sudo apt-get install -y xfonts-75dpi
sudo apt-get -f install
```
# Ubuntu 22.04 (jammy) khuyến nghị cài từ repo chính thức:
```bash
sudo dpkg -i ~/wkhtmltox_0.12.6.1-2.jammy_amd64.deb 
```
-link Wkhtml ( https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb )

-Lưu ý: tải file wkhtmltopdf phải đồng bộ theo version của ubuntu đang dùng( ở đây là bản 22)

## 8. cài đặt wkhtmltopdf

```bash
sudo apt install xvfb libfontconfig
```


- Trường hợp xảy ra lỗi 'E: Unmet dependencies. Try 'apt --fix-broken install' with no packages (or specify a solution).' 
thì tiến hành tải bản fix
``` bash
sudo apt --fix-broken install
```
- thực hiện lại lệnh chạy cài đặt gói 

```bash
sudo dpkg -i ~/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
```
## 9. Cài đặt Bench CLI
```bash
pip install frappe-bench
```
Lưu ý: tùy thuộc vào hệ điều hành và phiên bản Python, có thể cần sử dụng pip3 thay vì pip.

```bash
source ~/.profile
```
- tiếp tục thêm mục cài đặt vào biến môi trường PATH
```bash
echo "export PATH=/path/to/bin:$PATH" >> ~/.profile
source ~/.profile
```
- Lưu ý: tại bước thêm vào PATH , nếu xảy ra lỗi not a valid identifier :
    + mở thư mục .profile và tiến hành chỉnh sửa lại định dạng PATH
    sửa ~/.profile để bọc toàn bộ PATH trong dấu ngoặc kép, tránh lỗi export: 'Files/...': not a valid identifier do khoảng trắng trong “Program Files”.
định dạng của PATH trong file .profile sẽ tương tự như sau:
```bash
    # set PATH so it includes user's private bin if it exists
    if [ -d "$HOME/.local/bin" ] ; then
        PATH="$HOME/.local/bin:$PATH"
    fi
    export PATH="/path/to/bin:/home/minhmh/.local/bin:/home/minhmh/.nvm/versions/node/v22.21.1/bin:/home/minhmh/.cursor-server/bin/b3573281c4775bfc6bba466bf6563d3d498d1070/bin/remote-cli:/home/minhmh/.cursor-server/bin/b3573281c4775bfc6bba466bf6563d3d498d1070/bin/remote-cli:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Windows/system32:/mnt/c/Windows:/mnt/c/Windows/System32/Wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0/:/mnt/c/Windows/System32/OpenSSH/:/mnt/c/Program Files/cursor/resources/app/bin:/mnt/c/Users/Admin/AppData/Local/nvm:/mnt/c/nvm4w/nodejs:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/c/Users/Admin/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/Admin/AppData/Local/nvm:/mnt/c/nvm4w/nodejs:/snap/bin"
```
sau khi thay đổi PATH thì tiếp tục chạy lại lệnh trước đó và kiểm tra version để xem trạng thái đã cài đặt thành công hay chưa
```bash
source ~/.profile
bench --version
```
## 10.Khởi tạo bench theo  Frappe v15 :
```bash
bench init --frappe-branch version-15 frappe-demo
>> thư mục frappe-demo sẽ dđược khởi tạo
```
- Trường hợp xuất hiện lỗi ('CalledProcessError: Command 'python3 -m venv env' returned non-zero exit status 1. ') không khởi tạo đc init bench
Cài đặt lại môi trường py và thực hiện lại init
```bash
    sudo apt install python3.10-venv
    bench init --frappe-branch version-15 frappe-demo
```
## 11. Cài đặt Cài ERPNext và tiến hành tạo site mới

- Di chuyển tới thư mục frappe-demo vừa init và cài ERPNext
```bash
cd frappe-demo
bench get-app --branch version-15 erpnext
```
## 12. khởi tạo site mới
```bash
bench new-site demo.test
```
- Trường hợp xuất hiện lỗi mysql.err.OperationalError: (1698, "Access denied for user 'root'@'localhost'"):

```bash
sudo mysql
```

```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'yourpass';
FLUSH PRIVILEGES;
EXIT;
```
- Tiếp tục khởi tạo lại site 
```bash
bench new-site demo.test
```
## 13. thêm Host và cài ERPNext cho site
``` bash
bench --site demo.test add-to-hosts
bench --site demo.test install-app erpnext
```


## 14. Chạy server backend và kiểm tra

C:\Windows\System32\drivers\etc
open file host và thêm ip site vào dưới dòng localhos DNS

"127.0.0.1 demo.test"

```bash
bench start
```
- Giải thích: Khởi chạy các dịch vụ phát triển (web, worker, scheduler). Mặc định nghe ở cổng 8000.

Mở trình duyệt: `http://demo.test:8000/app/home` để kiểm tra ứng dụng đang chạy.

Lưu ý: Nếu gặp lỗi `ERROR: No process manager found`, cài và cấu hình process manager `honcho` rồi chạy lại:

```bash
pipx inject frappe-bench honcho
bench set-config -g process_manager honcho
bench setup procfile
bench start
```

(Xem chi tiết tại mục "Lỗi thường gặp" bên dưới.)

------------------end-------------------


## Một số lỗi thường gặp 


- ### Gỡ bỏ hoàn toàn và cài lại MariaDB (clean reinstall)

  Nếu bạn muốn xóa sạch MariaDB và cài lại từ đầu trên WSL Ubuntu:

  1) Dừng dịch vụ MariaDB (nếu đang chạy)

  ```bash
  sudo systemctl stop mariadb || true
  sudo systemctl stop mysql || true
  ```

  2) Gỡ bỏ gói và cấu hình liên quan

  ```bash
  sudo apt purge -y mariadb-server mariadb-client mariadb-common
  sudo apt autoremove -y
  sudo apt autoclean
  ```

  3) Xóa sạch dữ liệu và file cấu hình còn sót lại

  Cảnh báo: thao tác này sẽ xóa toàn bộ database hiện có trong máy local.

  ```bash
  sudo rm -rf /var/lib/mysql/
  sudo rm -rf /etc/mysql/
  sudo rm -rf /var/log/mysql/
  ```

  4) Cài đặt lại MariaDB 10.6 từ repo Ubuntu 22.04 (jammy)

  ```bash
  sudo apt update
  sudo apt install -y mariadb-server mariadb-client
  ```

  5) Chạy cấu hình bảo mật cơ bản

  ```bash
  sudo mysql_secure_installation
  ```

  6) Đặt các thông số khuyến nghị cho Frappe/ERPNext

  ```bash
  sudo mysql -u root <<'SQL'
  SET GLOBAL innodb_file_per_table=1;
  SET GLOBAL character_set_server = 'utf8mb4';
  SET GLOBAL collation_server = 'utf8mb4_unicode_ci';
  SQL
  ```

  7) Kiểm tra phiên bản và trạng thái

  ```bash
  mysql --version
  sudo systemctl status mariadb | cat
  ```

  8) Nếu cần đăng nhập bằng mật khẩu cho `root` (tránh plugin auth_socket), đổi plugin và đặt mật khẩu

  ```bash
  sudo mysql <<'SQL'
  ALTER USER 'root'@'localhost'
    IDENTIFIED VIA mysql_native_password
    USING PASSWORD('ReplaceWithYourRootPass');
  FLUSH PRIVILEGES;
  SQL
  ```

  9) Kiểm tra đăng nhập MySQL

  ```bash
  mysql -uroot -p'ReplaceWithYourRootPass' -e "SELECT VERSION();"
  ```

  10) Tiếp tục các bước tạo site và cài app ở mục 4) và 5) bên trên. Nếu gặp lỗi quyền khi tạo/cài site, xem các mục “MySQL: Access denied…” ngay bên dưới.

- MariaDB/Redis/wkhtmltopdf lỗi trên Windows: hãy dùng WSL Ubuntu.
- Sai phiên bản Python/MariaDB: dùng Python 3.10, MariaDB 10.6 cho ERPNext/Frappe v15.
- Lỗi CSRF khi dev Vite: thêm `"ignore_csrf": 1` trong `site_config.json`.
- Không thấy static sau build: đảm bảo đã chạy `yarn build` và có `education/www/student-portal.html`.
- Windows không resolve `education.test`: thêm vào hosts Windows như mục 5, rồi `ipconfig /flushdns`.
- Lỗi EPERM khi `yarn install` trên `/mnt/c`: sao chép dự án sang `~/education` trong WSL rồi cài.

### “Command 'bench' not found” sau khi cài bằng pipx

```bash
pipx ensurepath
source ~/.bashrc
which bench
bench --version
```
- Giải thích: Thêm `~/.local/bin` vào PATH và nạp lại shell. Nếu vẫn lỗi:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
which bench
```

### MySQL: `Access denied for user 'root'@'localhost'`

Nguyên nhân: root dùng plugin `auth_socket` (không nhận password) hoặc chưa đặt mật khẩu. Khắc phục:

1) Cách chuẩn MariaDB (đổi plugin + đặt mật khẩu trong 1 lệnh)

```bash
sudo mysql <<'SQL'
ALTER USER 'root'@'localhost'
  IDENTIFIED VIA mysql_native_password
  USING PASSWORD('RootPass!123');
FLUSH PRIVILEGES;
SQL
```

2) Cách thay thế (update plugin rồi đặt mật khẩu)

```bash
sudo mysql <<'SQL'
UPDATE mysql.user
  SET plugin='mysql_native_password'
  WHERE User='root' AND Host='localhost';
FLUSH PRIVILEGES;
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('RootPass!123');
FLUSH PRIVILEGES;
SQL
```

Kiểm tra:

```bash
mysql -uroot -p'ReplaceWithYourRootPass' -e "SELECT 1;"
```

Sử dụng khi tạo/reinstall site:

```bash
bench --site education.test reinstall --mariadb-root-username root --mariadb-root-password 'ReplaceWithYourRootPass' --yes
```

Lưu ý: nếu mật khẩu chứa ký tự `!`, hãy dùng here-doc như trên hoặc escape `!` thành `\!` để tránh lỗi bash “event not found”.

### MySQL: `Access denied for user '<site_db_user>'@'localhost'`

Khi `install-app` báo lỗi quyền với user DB của site, cấp quyền và đặt đúng mật khẩu theo `site_config.json` (ví dụ `db_name` = `_xxxx`, `db_password` = `YYYY`).

```bash
sudo mysql <<'SQL'
CREATE USER IF NOT EXISTS '_xxxx'@'localhost' IDENTIFIED BY 'YYYY';
CREATE USER IF NOT EXISTS '_xxxx'@'127.0.0.1' IDENTIFIED BY 'YYYY';
CREATE DATABASE IF NOT EXISTS `_xxxx` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON `_xxxx`.* TO '_xxxx'@'localhost';
GRANT ALL PRIVILEGES ON `_xxxx`.* TO '_xxxx'@'127.0.0.1';
FLUSH PRIVILEGES;
SQL
```

Kiểm tra kết nối bắt buộc TCP:

```bash
mysql --protocol=TCP -h 127.0.0.1 -u _xxxx -p'YYYY' _xxxx -e "SELECT 1;"
```

Nếu vẫn lỗi, có thể cấp thêm cho `%`:

```bash
sudo mysql -e "GRANT ALL PRIVILEGES ON `_xxxx`.* TO '_xxxx'@'%' IDENTIFIED BY 'YYYY'; FLUSH PRIVILEGES;"
```

### Lỗi: `Table '<db>.tabDefaultValue' doesn't exist` khi install-app

Nguyên nhân: schema Frappe chưa được tạo đầy đủ (site tạo chưa hoàn tất/do quyền DB). Khắc phục nhanh bằng reinstall site để Frappe tạo lại toàn bộ bảng:

```bash
bench --site education.test reinstall --mariadb-root-username root --mariadb-root-password 'ReplaceWithYourRootPass' --yes
# hoặc dùng user quản trị riêng:
bench --site education.test reinstall --mariadb-root-username frappe --mariadb-root-password 'StrongPass!123' --yes
```

Sau đó cài lại ứng dụng:

```bash
bench --site education.test install-app erpnext
bench --site education.test install-app education
```

### “No process manager found” khi `bench start`

Bench cần process manager. Dùng honcho như sau:

```bash
pipx inject frappe-bench honcho
bench set-config -g process_manager honcho
bench setup procfile
bench start
```

Kiểm tra cấu hình đã áp dụng:

```bash
grep process_manager -n sites/common_site_config.json
```

Nếu vẫn báo lỗi:

```bash
# 1) Đảm bảo honcho có trong PATH
which honcho || echo "honcho not found"
honcho --version || true

# 2) Thêm PATH từ pipx và nạp lại shell
pipx ensurepath
exec $SHELL -l
which honcho

# 3) (Fallback) Cài honcho vào user env
python3 -m pip install --user --upgrade honcho
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
which honcho

# 4) Tạo lại Procfile và thử lại
bench set-config -g process_manager honcho
bench setup procfile
bench start

# 5) (Tạm thời) Chạy trực tiếp bằng honcho để xác minh Procfile
honcho -f Procfile start
```

### MySQL: `Access denied for user 'root'@'localhost'` khi `bench new-site`

Trên Ubuntu, user `root` của MySQL có thể dùng plugin `auth_socket` (không nhận password). Có hai cách xử lý:

1) Đổi plugin xác thực cho root sang `mysql_native_password` và đặt mật khẩu:

```bash
sudo mysql
```
Trong MySQL shell:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_strong_password';
FLUSH PRIVILEGES;
```
Sau đó chạy lại:

```bash
bench new-site education.test
```
Khi được hỏi `MySQL root password`, nhập mật khẩu vừa đặt.

2) Hoặc tạo user quản trị riêng cho Frappe và dùng khi tạo site:

```bash
sudo mysql
```
Trong MySQL shell:

```sql
CREATE USER 'frappe'@'localhost' IDENTIFIED BY 'StrongPass!123';
GRANT ALL PRIVILEGES ON *.* TO 'frappe'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```
Tạo site với tham số chỉ định user/password MySQL:

```bash
bench new-site education.test --mariadb-root-username frappe --mariadb-root-password 'StrongPass!123'
```
- Giải thích: Dùng user `frappe` làm tài khoản có quyền tạo DB/schema thay vì root.


