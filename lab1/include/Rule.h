#pragma once

#include <string>

/**
 * @brief Представляет одно правило в алгоритме Маркова: "образец → результат".
 * Правило применяется к строке, если образец найден.
 */
class Rule {
public:
    /**
     * @brief Конструктор по умолчанию (создаёт пустое правило).
     */
    Rule();

    /**
     * @brief Конструктор с параметрами.
     * @param pattern Образец для поиска в строке.
     * @param result Строка, на которую заменяется образец.
     */
    Rule(const std::string& pattern, const std::string& result);

    /**
     * @brief Сравнение двух правил на равенство.
     */
    bool operator==(const Rule& other) const;

    // Геттеры
    const std::string& getPattern() const noexcept;
    const std::string& getResult() const noexcept;

private:
    std::string pattern_;
    std::string result_;
};
