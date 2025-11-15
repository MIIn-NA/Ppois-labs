#include "Rule.h"

Rule::Rule() : pattern_(""), result_("") {}

Rule::Rule(const std::string& pattern, const std::string& result)
    : pattern_(pattern), result_(result) {}

bool Rule::operator==(const Rule& other) const {
    return pattern_ == other.pattern_ && result_ == other.result_;
}

const std::string& Rule::getPattern() const noexcept {
    return pattern_;
}

const std::string& Rule::getResult() const noexcept {
    return result_;
}
