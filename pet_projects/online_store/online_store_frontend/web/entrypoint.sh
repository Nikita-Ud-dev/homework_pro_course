#!/bin/sh

set -e

echo "Запускаємо контейнер Frontend..."


if [ ! -d "node_modules" ] || [ -z "$(ls -A node_modules 2>/dev/null)" ]; then
  echo "Встановлюємо залежності..."
  npm ci || npm install
fi

echo "Запускаємо Vite..."
exec npm run dev -- --host 0.0.0.0 --port 5173
