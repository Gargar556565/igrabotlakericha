// Сервер для раздачи статических файлов Mini App
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  let url = (req.url || '/').split('?')[0].replace(/^\/+/, '') || 'index.html';
  const publicDir = path.join(__dirname, 'public');
  const filePath = path.join(publicDir, path.normalize(url));
  const resolvedPath = path.resolve(filePath);
  const resolvedPublic = path.resolve(publicDir);

  if (!resolvedPath.startsWith(resolvedPublic + path.sep) && resolvedPath !== resolvedPublic) {
    res.writeHead(403);
    res.end('Доступ запрещён');
    return;
  }

  const extname = path.extname(resolvedPath);
  const contentType = mimeTypes[extname] || 'text/plain';

  fs.readFile(resolvedPath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404);
        res.end('Файл не найден');
      } else {
        res.writeHead(500);
        res.end('Ошибка сервера: ' + error.code);
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log('✅ Сервер запущен на порту ' + PORT);
});
