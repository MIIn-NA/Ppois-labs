#!/bin/bash

# Очистка
rm -f *.gcda *.gcno *.info
rm -rf coverage_report/
find . -name "*.gcda" -delete
find . -name "*.gcno" -delete

# Сборка
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
if [ $? -ne 0 ]; then
    echo "Ошибка сборки"
    exit 1
fi


./build/markov_tests --gtest_brief || true


lcov --base-directory . \
     --directory build \
     --capture \
     --output-file coverage.info \
     --no-external \
     --ignore-errors mismatch,empty,gcov,unused


lcov --remove coverage.info \
     '*/tests/*' \
     '*/gtest/*' \
     '/usr/*' \
     '*/CMakeFiles/*' \
     --output-file coverage_filtered.info \
     --ignore-errors mismatch,empty,gcov,unused


genhtml --output-directory coverage_report coverage_filtered.info --ignore-errors empty

COVERAGE_PERCENT=$(lcov --summary coverage_filtered.info 2>/dev/null | grep "lines.*:" | awk '{print $2}' | tr -d '%')
if [[ -n "$COVERAGE_PERCENT" ]]; then
    echo "=================================="
    echo "Общее покрытие кода: ${COVERAGE_PERCENT}%"
    echo "Отчёт: coverage_report/index.html"
    echo "=================================="
else
    echo "Не удалось определить процент покрытия."
fi
