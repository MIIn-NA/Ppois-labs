#include "Set.h"
#include <stdexcept>
#include <cctype>
#include <algorithm>

Set::Element::Element() : type(VALUE) {}
Set::Element::Element(const std::string& value) : type(VALUE), atom(value) {}
Set::Element::Element(const std::vector<Element>& nested) : type(NESTED_SET), subset(nested) {}

bool operator==(const Set::Element& lhs, const Set::Element& rhs) {
    if (lhs.type != rhs.type) return false;
    if (lhs.type == Set::VALUE) return lhs.atom == rhs.atom;
    if (lhs.type == Set::NESTED_SET) {
        Set tempA(lhs.subset);
        Set tempB(rhs.subset);
        return tempA == tempB;
    }
    return false;
}

bool operator!=(const Set::Element& lhs, const Set::Element& rhs) {
    return !(lhs == rhs);
}

Set::Set() = default;

Set::Set(const std::string& serialized) {
    loadFromString(serialized);
}

Set::Set(const std::vector<Element>& items) : storage_(items) {
    eliminateDuplicates();
}

Set::Set(const Set& other) : storage_(other.storage_) {}

Set& Set::operator=(const Set& other) {
    if (this != &other) {
        storage_ = other.storage_;
    }
    return *this;
}

bool Set::contains(const Element& item) const {
    for (const auto& el : storage_) {
        if (el == item) return true;
    }
    return false;
}

bool Set::isEmpty() const {
    return storage_.empty();
}

std::size_t Set::size() const {
    return storage_.size();
}

void Set::insert(const Element& item) {
    if (!contains(item)) {
        storage_.push_back(item);
    }
}

void Set::erase(const Element& item) {
    storage_.erase(
        std::remove_if(storage_.begin(), storage_.end(),
            [&item](const Element& current) { return current == item; }),
        storage_.end()
    );
}

Set Set::unite(const Set& other) const {
    Set result(*this);
    for (const auto& element : other.storage_) {
        result.insert(element);
    }
    return result;
}

Set& Set::selfUnite(const Set& other) {
    for (const auto& element : other.storage_) {
        insert(element);
    }
    return *this;
}

Set Set::intersect(const Set& other) const {
    Set result;
    for (const auto& element : storage_) {
        if (other.contains(element)) {
            result.insert(element);
        }
    }
    return result;
}

Set& Set::selfIntersect(const Set& other) {
    std::vector<Element> intersection;
    for (const auto& element : storage_) {
        if (other.contains(element)) {
            intersection.push_back(element);
        }
    }
    storage_ = intersection;
    return *this;
}

Set Set::difference(const Set& other) const {
    Set result;
    for (const auto& element : storage_) {
        if (!other.contains(element)) {
            result.insert(element);
        }
    }
    return result;
}

Set& Set::selfDifference(const Set& other) {
    storage_.erase(
        std::remove_if(storage_.begin(), storage_.end(),
            [&other](const Element& element) { return other.contains(element); }),
        storage_.end()
    );
    return *this;
}

bool Set::operator==(const Set& other) const {
    if (storage_.size() != other.storage_.size()) return false;
    for (const auto& element : storage_) {
        if (!other.contains(element)) return false;
    }
    return true;
}

bool Set::operator!=(const Set& other) const {
    return !(*this == other);
}

bool Set::has(const Element& item) const {
    return contains(item);
}

Set Set::powerSet() const {
    Set result;
    result.insert(Element(std::vector<Element>()));
    std::size_t n = storage_.size();
    std::size_t total = 1ULL << n;
    for (std::size_t i = 1; i < total; ++i) {
        std::vector<Element> subset;
        for (std::size_t j = 0; j < n; ++j) {
            if (i & (1ULL << j)) {
                subset.push_back(storage_[j]);
            }
        }
        result.insert(Element(subset));
    }
    return result;
}

Set::Element Set::parseAtomic(const std::string& str, std::size_t& index) const {
    while (index < str.size() && isWhitespace(str[index])) ++index;
    if (index < str.size() && str[index] == '{') {
        return parseGroup(str, index);
    }
    std::string token;
    while (index < str.size() && str[index] != ',' && str[index] != '}' && !isWhitespace(str[index])) {
        if (str[index] == '{') {
            throw std::invalid_argument("Unexpected '{' inside token");
        }
        token += str[index];
        ++index;
    }
    for (char ch : token) {
        if (!isDigit(ch) && !isLetter(ch) && ch != '_') {
            throw std::invalid_argument("Invalid character: " + std::string(1, ch));
        }
    }
    return Element(token);
}

Set::Element Set::parseGroup(const std::string& str, std::size_t& index) const {
    if (str[index] != '{') {
        throw std::invalid_argument("Expected '{'");
    }
    ++index;
    std::vector<Element> items;
    while (index < str.size()) {
        while (index < str.size() && isWhitespace(str[index])) ++index;
        if (index < str.size() && str[index] == '}') {
            ++index;
            break;
        }
        Element el = parseAtomic(str, index);
        items.push_back(el);
        while (index < str.size() && isWhitespace(str[index])) ++index;
        if (index < str.size() && str[index] == ',') {
            ++index;
        } else if (index < str.size() && str[index] != '}') {
            throw std::invalid_argument("Expected ',' or '}'");
        }
    }
    return Element(items);
}

void Set::loadFromString(const std::string& input) {
    storage_.clear();
    std::string clean = input;
    clean.erase(std::remove_if(clean.begin(), clean.end(),
        [this](char c) { return isWhitespace(c); }), clean.end());
    
    // Исправлено: проверка на пустую строку и корректность формата
    if (clean.empty() || clean[0] != '{' || clean.back() != '}') {
        throw std::invalid_argument("Invalid set format");
    }
    
    std::size_t pos = 0;
    Element root = parseGroup(clean, pos);
    
    // Исправлено: проверка что весь вход был обработан
    if (pos != clean.size()) {
        throw std::invalid_argument("Unexpected characters at the end");
    }
    
    storage_ = root.subset;
    eliminateDuplicates();
}

void Set::eliminateDuplicates() {
    std::vector<Element> unique;
    for (const auto& elem : storage_) {
        bool found = false;
        for (const auto& u : unique) {
            if (u == elem) {
                found = true;
                break;
            }
        }
        if (!found) {
            unique.push_back(elem);
        }
    }
    storage_ = unique;
}

std::string Set::stringifyElement(const Element& elem) const {
    if (elem.type == VALUE) return elem.atom;
    std::string result = "{";
    for (std::size_t i = 0; i < elem.subset.size(); ++i) {
        result += stringifyElement(elem.subset[i]);
        if (i < elem.subset.size() - 1) result += ", ";
    }
    result += "}";
    return result;
}

bool Set::isWhitespace(char c) const {
    // Исправлено: добавлен недостающий оператор ||
    return c == ' ' || c == '\t' || c == '\r' || c == '\n';
}

bool Set::isDigit(char c) const {
    return std::isdigit(static_cast<unsigned char>(c));
}

bool Set::isLetter(char c) const {
    return std::isalpha(static_cast<unsigned char>(c));
}

std::string Set::serialize() const {
    if (isEmpty()) return "{}";
    std::string result = "{";
    for (std::size_t i = 0; i < storage_.size(); ++i) {
        result += stringifyElement(storage_[i]);
        if (i < storage_.size() - 1) result += ", ";
    }
    result += "}";
    return result;
}

Set Set::deserialize(const std::string& input) {
    return Set(input);
}

std::ostream& operator<<(std::ostream& os, const Set& set) {
    os << set.serialize();
    return os;
}

std::istream& operator>>(std::istream& is, Set& set) {
    std::string line;
    std::getline(is, line);
    set = Set::deserialize(line);
    return is;
}
