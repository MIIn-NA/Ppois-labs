#!/bin/bash

set -e

# Создаем и переходим в директорию сборки
mkdir -p build
cd build

# Конфигурируем проект с включенной поддержкой покрытия
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="--coverage -fprofile-arcs -ftest-coverage" ..

# Собираем проект
make

# Запускаем тесты
echo "Запуск тестов..."
./set_tests

# Создаем директорию для отчета
mkdir -p coverage_report

# Используем gcovr для анализа покрытия
echo "Анализ покрытия с помощью gcovr..."
gcovr -r .. \
    --exclude=".*tests.*" \
    --exclude=".*googletest.*" \
    --exclude=".*/usr/.*" \
    --html \
    --html-details \
    -o coverage_report/coverage.html

# Получаем общий процент покрытия
COVERAGE_PERCENT=$(gcovr -r .. \
    --exclude=".*tests.*" \
    --exclude=".*googletest.*" \
    --exclude=".*/usr/.*" \
    --print-summary | grep -oP 'lines: \K[0-9.]+' | head -1 || echo "0")

echo "=================================="
echo "Общее покрытие кода: ${COVERAGE_PERCENT}%"
echo "Отчёт: coverage_report/coverage.html"
echo "=================================="
