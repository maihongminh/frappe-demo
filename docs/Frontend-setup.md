# Hướng Dẫn Setup Frontend cho firt_demo


Module `firt_demo` sử dụng **Vue 3** với **Vite** làm build tool. Frontend được tích hợp vào Frappe framework thông qua template HTML và assets.

## Cấu Trúc Thư Mục Cần Có

```
firt_demo/
├── firt_demo/
│   ├── frontend/          # Source code Vue (development)
│   │   ├── src/
│   │   │   ├── main.js    # Entry point Vue app
│   │   │   ├── App.vue    # Root component
│   │   │   └── components/
│   │   ├── node_modules/  # Dependencies (tự động tạo khi npm install)
│   │   ├── package.json   # Khai báo dependencies
│   │   ├── package-lock.json # Lock file (tự động tạo)
│   │   └── vite.config.js # Vite configuration
│   ├── public/
│   │   └── frontend/      # Build output (production)
│   │       └── js/
│   │           └── main.js
│   └── www/
│       └── vue_demo.html  # Template page
```

## Các Bước Setup Frontend

### Bước 1: Kiểm Tra Node.js và npm

Đảm bảo đã cài đặt Node.js (phiên bản 14 trở lên):

```bash
node --version
npm --version
```

Nếu chưa có, cài đặt Node.js:
```bash
# Trên Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Bước 2: Di Chuyển Đến Thư Mục Frontend

```bash
cd /home/minhmh/frappe-demo/apps/firt_demo/firt_demo/frontend
```

### Bước 3: Cài Đặt Dependencies

Cài đặt các package cần thiết từ `package.json`:

```bash
npm install
```

Lệnh này sẽ cài đặt:
- `vue` (^3.3.0) - Vue 3 framework
- `vite` (^4.0.0) - Build tool
- `@vitejs/plugin-vue` (^4.0.0) - Vite plugin cho Vue

**Sau khi chạy `npm install`, thư mục `node_modules` sẽ được tạo ra tự động.**

### Giải Thích Về node_modules

#### node_modules là gì?

`node_modules` là thư mục chứa tất cả các package/dependencies mà dự án của bạn cần. Khi bạn chạy `npm install`, npm sẽ:
1. Đọc file `package.json`
2. Tải về các package được khai báo
3. Cài đặt chúng vào thư mục `node_modules`
4. Tạo file `package-lock.json` để lock phiên bản chính xác

#### Cấu Trúc Sau Khi Cài Đặt

```
frontend/
├── node_modules/          # Thư mục chứa tất cả dependencies (TỰ ĐỘNG TẠO)
│   ├── vue/               # Vue framework
│   ├── vite/               # Vite build tool
│   ├── @vitejs/
│   │   └── plugin-vue/     # Vite plugin cho Vue
│   └── ...                 # Các dependencies khác
├── package-lock.json       # Lock file (TỰ ĐỘNG TẠO)
├── package.json            # File khai báo dependencies
├── vite.config.js
└── src/
```

#### Lưu Ý Quan Trọng

1. **KHÔNG commit `node_modules` vào Git**
   - Thư mục này rất lớn (có thể hàng trăm MB)
   - Có thể tái tạo lại bằng `npm install`
   - Thêm vào `.gitignore`:
     ```bash
     echo "node_modules/" >> .gitignore
     ```

2. **Khi nào cần xóa `node_modules`?**
   - Khi gặp lỗi "module not found"
   - Khi cập nhật dependencies
   - Khi chuyển máy/môi trường mới
   ```bash
   rm -rf node_modules
   npm install
   ```

3. **Kích thước của node_modules**
   - `node_modules` thường rất lớn (50-200MB hoặc hơn)
   - Chỉ cần thiết trong quá trình development và build
   - Không cần thiết trong production (chỉ cần file build output)

4. **package-lock.json**
   - File này sẽ được tạo tự động
   - Nên commit vào Git để đảm bảo mọi người dùng cùng phiên bản


#### Kiểm Tra node_modules Đã Được Cài Đặt Chưa

```bash
# Kiểm tra thư mục có tồn tại không
ls -la node_modules/

# Kiểm tra các package đã cài
ls node_modules/ | head -20

# Kiểm tra kích thước
du -sh node_modules/
```

### Bước 4: Cấu Hình Git (Quan Trọng)

Đảm bảo `node_modules` không được commit vào Git:

```bash
cd /home/minhmh/frappe-demo/apps/firt_demo/firt_demo/frontend

# Kiểm tra file .gitignore có tồn tại không
ls -la .gitignore

# Nếu chưa có, tạo file .gitignore
cat > .gitignore << EOF
# Dependencies
node_modules/
package-lock.json

# Build output
../public/frontend/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Editor directories
.vscode/
.idea/
*.swp
*.swo
EOF
```

**Lưu ý**: 
- `package-lock.json` thường NÊN commit để đảm bảo mọi người dùng cùng phiên bản
- `node_modules` KHÔNG NÊN commit vì quá lớn và có thể tái tạo

### Bước 5: Kiểm Tra Cấu Hình Vite

File `vite.config.js` đã được cấu hình để:
- Build output vào `../public/frontend`
- Entry point: `src/main.js`
- Output file: `js/main.js`

### Bước 6: Build Frontend cho Production

Sau khi cài đặt dependencies, build frontend:

```bash
npm run build
```

Lệnh này sẽ:
1. Compile Vue components
2. Bundle JavaScript
3. Output vào `firt_demo/public/frontend/js/main.js`

**Lưu ý**: Build process sẽ sử dụng các package trong `node_modules` để compile code.

### Bước 7: Kiểm Tra Template HTML

File `www/vue_demo.html` đã được cấu hình để:
- Load script từ `/assets/firt_demo/frontend/js/main.js`
- Mount Vue app vào element `#vue-app`
**Lưu ý**: 
   + Frappe sẽ tự động scan thư mục www/
   + Mỗi file .html sẽ trở thành một route
   + Không cần cấu hình thêm trong hooks.py (trừ khi cần custom logic)
**Quy tắc đặt tên route:**
- Tên file (không có extension `.html`) = URL path
- Ví dụ: `vue_demo.html` → URL: `http://your-site:8000/vue_demo`
- Ví dụ: `about.html` → URL: `http://your-site:8000/about`
- Ví dụ: `contact.html` → URL: `http://your-site:8000/contact`

### Bước 8: Build Assets trong Frappe

Sau khi build frontend, cần build assets trong Frappe:

```bash
cd /home/minhmh/frappe-demo
bench build --app firt_demo
```

Hoặc build tất cả assets:
```bash
bench build
```

### Bước 9: Restart Frappe (nếu cần)

```bash
bench restart
```

### Bước 10: Truy Cập Trang Vue Demo

Mở trình duyệt và truy cập:
```
http://your-site:8000/vue_demo
```

## Development Workflow

### Chế Độ Development (Hot Reload)

Để phát triển với hot reload, bạn có thể chạy Vite dev server:

```bash
cd /home/minhmh/frappe-demo/apps/firt_demo/firt_demo/frontend
npm run dev
```

**Lưu ý**: Vite dev server chạy trên port riêng (thường là 5173). Để tích hợp với Frappe, bạn cần:
1. Cấu hình proxy trong Frappe
2. Hoặc build sau mỗi lần thay đổi

### Workflow Khuyến Nghị

1. **Phát triển**:
   ```bash
   cd firt_demo/frontend
   # Chỉnh sửa code trong src/
   npm run build
   bench build --app firt_demo
   bench restart
   ```

2. **Sử dụng watch mode** (tự động build khi có thay đổi):
   ```bash
   # Cài đặt nodemon hoặc sử dụng Vite watch
   npm install --save-dev nodemon
   # Thêm script vào package.json:
   # "watch": "vite build --watch"
   ```

## Cấu Trúc Code

### main.js
```javascript
import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

// Mount khi frappe sẵn sàng
frappe.ready(() => {
    const mountPoint = document.getElementById('vue-app');
    if (mountPoint) {
        app.mount('#vue-app');
    }
});
```

### App.vue
Component gốc của ứng dụng Vue.
 Vd:
```javascript
<template>
	<div class="container mt-5">
		<h1 class="mb-4">firt_demo Vue App</h1>
		<p class="lead">
			Hello world.
		</p>
	</div>
</template>

<script>
export default {
	name: 'App',
};
</script>
```

### vite.config.js
Cấu hình build output vào `public/frontend` để Frappe có thể serve assets.


### Lỗi: Module not found

Khi gặp lỗi này, thường do `node_modules` bị thiếu hoặc hỏng:

```bash
cd firt_demo/frontend

# Xóa node_modules và package-lock.json
rm -rf node_modules package-lock.json

# Cài lại tất cả dependencies
npm install

# Kiểm tra lại
ls node_modules/ | grep vue
```

### Lỗi: node_modules quá lớn hoặc chiếm nhiều dung lượng

`node_modules` có thể rất lớn (50-200MB). Đây là bình thường. Nếu cần tiết kiệm dung lượng:

```bash
# Xóa node_modules khi không cần thiết (sau khi đã build xong)
rm -rf node_modules

# Khi cần lại, chỉ cần chạy:
npm install
```

**Lưu ý**: Chỉ xóa `node_modules` khi bạn đã build xong và không cần development nữa.

### Lỗi: Build không tạo file
- Kiểm tra đường dẫn output trong `vite.config.js`
- Đảm bảo thư mục `public/frontend` tồn tại

### Lỗi: Script không load trong browser
- Kiểm tra `bench build --app firt_demo` đã chạy chưa
- Kiểm tra console browser để xem lỗi
- Đảm bảo đường dẫn trong `vue_demo.html` đúng: `/assets/firt_demo/frontend/js/main.js`

### Lỗi: Vue app không mount
- Kiểm tra element `#vue-app` có trong HTML không
- Kiểm tra `frappe.ready()` có được gọi không
- Mở console browser để debug

## Tóm Tắt Các Lệnh Quan Trọng

```bash
# 1. Cài đặt dependencies
cd firt_demo/frontend
npm install

# 2. Build frontend
npm run build

# 3. Build Frappe assets
cd ../../../
bench build --app firt_demo

# 4. Restart (nếu cần)
bench restart
```

## Tài Liệu Tham Khảo

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Frappe Framework](https://frappeframework.com/)

