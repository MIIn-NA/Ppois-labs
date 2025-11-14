#pragma once

#include <string>
#include <vector>
#include <fstream>
#include "Rule.h"

class Markov {
public:
    Markov();
    explicit Markov(const std::string& filename);
    void execute(bool log = false);
    void addTransformationRule(const std::string& pattern, const std::string& result);
    bool removeTransformationRule(const std::string& pattern, const std::string& result);
    bool modifyRuleAt(size_t index, const std::string& newPattern, const std::string& newResult);
    void loadRulesFromFile(const std::string& filename);
    void displayRules() const;
    const std::string& getCurrentString() const noexcept;
    void setStartString(const std::string& start);
    bool applySingleStep();

private:
    std::vector<Rule> transformationRules_;
    std::string currentString_;
    bool applyFirstMatchingRule();
};
