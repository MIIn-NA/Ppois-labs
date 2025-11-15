#pragma once

#include <iostream>
#include <string>
#include <vector>

class Set {
public:
    enum ElementType {
        VALUE,
        NESTED_SET
    };

    struct Element {
        ElementType type;
        std::string atom;
        std::vector<Element> subset;

        Element();
        Element(const std::string& value);
        Element(const std::vector<Element>& nested);

        friend bool operator==(const Element& lhs, const Element& rhs);
        friend bool operator!=(const Element& lhs, const Element& rhs);
    };

    // Конструкторы и присваивание
    Set();
    explicit Set(const std::string& serialized);
    explicit Set(const std::vector<Element>& items);
    Set(const Set& other);
    ~Set() = default;

    Set& operator=(const Set& other);

    // Основные методы
    bool contains(const Element& item) const;
    bool isEmpty() const;
    std::size_t size() const;
    void insert(const Element& item);
    void erase(const Element& item);

    // Операции над множествами
    Set unite(const Set& other) const;
    Set& selfUnite(const Set& other);
    Set intersect(const Set& other) const;
    Set& selfIntersect(const Set& other);
    Set difference(const Set& other) const;
    Set& selfDifference(const Set& other);

    // Сравнение
    bool operator==(const Set& other) const;
    bool operator!=(const Set& other) const;
    bool has(const Element& item) const;

    // Булеан
    Set powerSet() const;

    // Сериализация
    std::string serialize() const;
    static Set deserialize(const std::string& input);

    // Потоковые операторы (дружественные функции)
    friend std::ostream& operator<<(std::ostream& os, const Set& set);
    friend std::istream& operator>>(std::istream& is, Set& set);

private:
    std::vector<Element> storage_;

    // Внутренние методы парсинга
    Element parseAtomic(const std::string& str, std::size_t& index) const;
    Element parseGroup(const std::string& str, std::size_t& index) const;
    void loadFromString(const std::string& str);

    // Вспомогательные методы
    void eliminateDuplicates();
    std::string stringifyElement(const Element& elem) const;
    bool isWhitespace(char c) const;
    bool isDigit(char c) const;
    bool isLetter(char c) const;
};
