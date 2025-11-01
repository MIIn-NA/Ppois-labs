#ifndef SETLIB_SET_H
#define SETLIB_SET_H

#include <iostream>
#include <memory>
#include <string>
#include <variant>
#include <vector>

class Set; // forward declaration

/// Represents a single element of a Set: integer, string, or another Set.
class SetElement {
public:
    using PtrSet = std::shared_ptr<Set>;
    using Value  = std::variant<long, std::string, PtrSet>;

    SetElement();
    explicit SetElement(long v);
    explicit SetElement(std::string v);
    explicit SetElement(const Set& s);
    explicit SetElement(PtrSet nested);

    SetElement(const SetElement&) = default;
    SetElement& operator=(const SetElement&) = default;
    ~SetElement() = default;

    bool isNumber() const;
    bool isString() const;
    bool isSet() const;

    const Value& value() const { return value_; }

    bool operator==(const SetElement& other) const;
    bool operator!=(const SetElement& other) const { return !(*this == other); }

    std::string toString() const;

private:
    Value value_;
};

/// Mathematical Set supporting nested sets and basic operations.
class Set {
public:
    Set() = default;

    Set(const Set& other);
    Set& operator=(const Set& other);
    ~Set() = default;

    bool add(const SetElement& el);
    bool remove(const SetElement& el);
    bool contains(const SetElement& el) const;

    size_t size() const { return elements_.size(); }
    bool isEmpty() const { return elements_.empty(); }

    static Set unionWith(const Set& a, const Set& b);
    static Set intersectionWith(const Set& a, const Set& b);
    static Set differenceWith(const Set& a, const Set& b);

    bool subsetOf(const Set& other) const;

    bool operator==(const Set& other) const;
    bool operator!=(const Set& other) const { return !(*this == other); }

    std::string toString() const;
    static Set fromString(const std::string& text);

    friend std::ostream& operator<<(std::ostream& os, const Set& s) {
        return os << s.toString();
    }
    friend std::istream& operator>>(std::istream& is, Set& s);

private:
    std::vector<SetElement> elements_;

    static bool equalElement(const SetElement& a, const SetElement& b);
    static bool elementLessForStableOrder(const SetElement& a, const SetElement& b);
    void normalize();
};

#endif // SETLIB_SET_H
