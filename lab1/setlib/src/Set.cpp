#include "Set.h"
#include <algorithm>
#include <cctype>
#include <sstream>
#include <stdexcept>

// ===== SetElement =====

SetElement::SetElement() : value_(0L) {}
SetElement::SetElement(long v) : value_(v) {}
SetElement::SetElement(std::string v) : value_(std::move(v)) {}
SetElement::SetElement(const Set& s) : value_(std::make_shared<Set>(s)) {}
SetElement::SetElement(PtrSet nested) : value_(std::move(nested)) {}

bool SetElement::isNumber() const { return std::holds_alternative<long>(value_); }
bool SetElement::isString() const { return std::holds_alternative<std::string>(value_); }
bool SetElement::isSet() const { return std::holds_alternative<PtrSet>(value_); }

bool SetElement::operator==(const SetElement& other) const {
    if (value_.index() != other.value_.index()) return false;
    if (isNumber()) return std::get<long>(value_) == std::get<long>(other.value_);
    if (isString()) return std::get<std::string>(value_) == std::get<std::string>(other.value_);
    return *std::get<PtrSet>(value_) == *std::get<PtrSet>(other.value_);
}

std::string SetElement::toString() const {
    if (isNumber()) return std::to_string(std::get<long>(value_));
    if (isString()) return '"' + std::get<std::string>(value_) + '"';
    return std::get<PtrSet>(value_)->toString();
}

// ===== Set =====

Set::Set(const Set& other) : elements_(other.elements_) {}
Set& Set::operator=(const Set& other) {
    if (this != &other) elements_ = other.elements_;
    return *this;
}

bool Set::equalElement(const SetElement& a, const SetElement& b) { return a == b; }

static int tag(const SetElement& e) {
    if (e.isNumber()) return 0;
    if (e.isString()) return 1;
    return 2;
}

bool Set::elementLessForStableOrder(const SetElement& a, const SetElement& b) {
    int ta = tag(a), tb = tag(b);
    if (ta != tb) return ta < tb;
    if (a.isNumber()) return std::get<long>(a.value()) < std::get<long>(b.value());
    if (a.isString()) return std::get<std::string>(a.value()) < std::get<std::string>(b.value());
    return a.toString() < b.toString();
}

void Set::normalize() {
    std::sort(elements_.begin(), elements_.end(), elementLessForStableOrder);
    elements_.erase(std::unique(elements_.begin(), elements_.end(), equalElement), elements_.end());
}

bool Set::add(const SetElement& el) {
    if (contains(el)) return false;
    elements_.push_back(el);
    normalize();
    return true;
}

bool Set::remove(const SetElement& el) {
    auto it = std::remove_if(elements_.begin(), elements_.end(),
                             [&](const SetElement& x){ return x == el; });
    bool removed = it != elements_.end();
    elements_.erase(it, elements_.end());
    return removed;
}

bool Set::contains(const SetElement& el) const {
    return std::any_of(elements_.begin(), elements_.end(),
                       [&](const SetElement& x){ return x == el; });
}

Set Set::unionWith(const Set& a, const Set& b) {
    Set r = a;
    for (const auto& e : b.elements_) r.add(e);
    r.normalize();
    return r;
}

Set Set::intersectionWith(const Set& a, const Set& b) {
    Set r;
    for (const auto& e : a.elements_)
        if (b.contains(e)) r.add(e);
    return r;
}

Set Set::differenceWith(const Set& a, const Set& b) {
    Set r;
    for (const auto& e : a.elements_)
        if (!b.contains(e)) r.add(e);
    return r;
}

bool Set::subsetOf(const Set& other) const {
    for (const auto& e : elements_)
        if (!other.contains(e)) return false;
    return true;
}

bool Set::operator==(const Set& other) const {
    if (elements_.size() != other.elements_.size()) return false;
    for (size_t i = 0; i < elements_.size(); ++i)
        if (!(elements_[i] == other.elements_[i])) return false;
    return true;
}

std::string Set::toString() const {
    std::ostringstream oss;
    oss << '{';
    for (size_t i = 0; i < elements_.size(); ++i) {
        if (i) oss << ", ";
        oss << elements_[i].toString();
    }
    oss << '}';
    return oss.str();
}

// === Parsing ===
namespace {
struct Lexer {
    const std::string& s;
    size_t i{0};
    explicit Lexer(const std::string& str) : s(str) {}
    void skip() { while (i < s.size() && std::isspace((unsigned char)s[i])) ++i; }
    bool eat(char c) { skip(); if (i < s.size() && s[i] == c) { ++i; return true; } return false; }
    void expect(char c) { if (!eat(c)) throw std::runtime_error(std::string("Expected '") + c + "'"); }
};

Set parseSet(Lexer& L);

SetElement parseElem(Lexer& L) {
    L.skip();
    if (L.i >= L.s.size()) throw std::runtime_error("Unexpected end of input");
    char c = L.s[L.i];
    if (c == '{') {
        Set nested = parseSet(L);
        return SetElement(std::make_shared<Set>(nested));
    }
    if (c == '"') {
        ++L.i;
        std::string out;
        bool closed = false;
        while (L.i < L.s.size()) {
            char d = L.s[L.i++];
            if (d == '"') { closed = true; break; }
            out.push_back(d);
        }
        if (!closed) throw std::runtime_error("Unterminated string literal");
        return SetElement(out);
    }
    bool neg = false;
    if (c == '-') { neg = true; ++L.i; }
    long val = 0;
    bool any = false;
    while (L.i < L.s.size() && std::isdigit((unsigned char)L.s[L.i])) {
        any = true;
        val = val * 10 + (L.s[L.i++] - '0');
    }
    if (!any) throw std::runtime_error("Expected number or string or set");
    return SetElement(neg ? -val : val);
}

Set parseSet(Lexer& L) {
    Set res;
    L.expect('{');
    L.skip();
    if (L.eat('}')) return res;
    while (true) {
        auto el = parseElem(L);
        res.add(el);
        L.skip();
        if (L.eat('}')) break;
        L.expect(',');
    }
    return res;
}
} // namespace

Set Set::fromString(const std::string& text) {
    Lexer L(text);
    return parseSet(L);
}

std::istream& operator>>(std::istream& is, Set& s) {
    std::string input;
    std::getline(is, input);
    s = Set::fromString(input);
    return is;
}
