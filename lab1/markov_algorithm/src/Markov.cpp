#include "Markov.h"
#include <iostream>
#include <sstream>
#include <cctype>

static std::string trim(const std::string& str) {
    size_t start = str.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return "";
    size_t end = str.find_last_not_of(" \t\r\n");
    return str.substr(start, end - start + 1);
}

Markov::Markov() : currentString_("") {}

Markov::Markov(const std::string& filename) {
    loadRulesFromFile(filename);
}

void Markov::execute(bool log) {
    int counter = 0;
    const int maxIterations = 1000;
    while (counter < maxIterations && applyFirstMatchingRule()) {
        counter++;
        if (log) {
            std::cout << currentString_ << std::endl;
        }
    }
}

void Markov::addTransformationRule(const std::string& pattern, const std::string& result) {
    Rule newRule(pattern, result);
    for (const auto& rule : transformationRules_) {
        if (rule == newRule) {
            return;
        }
    }
    transformationRules_.push_back(newRule);
}

bool Markov::removeTransformationRule(const std::string& pattern, const std::string& result) {
    Rule target(pattern, result);
    for (auto it = transformationRules_.begin(); it != transformationRules_.end(); ++it) {
        if (*it == target) {
            transformationRules_.erase(it);
            return true;
        }
    }
    return false;
}

bool Markov::modifyRuleAt(size_t index, const std::string& newPattern, const std::string& newResult) {
    if (index >= transformationRules_.size()) {
        return false;
    }
    transformationRules_[index] = Rule(newPattern, newResult);
    return true;
}

void Markov::loadRulesFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        return;
    }

    std::string line;
    if (std::getline(file, line)) {
        currentString_ = trim(line);
    }

    while (std::getline(file, line)) {
        line = trim(line);
        if (line.empty()) continue;

        size_t arrowPos = line.find("->");
        if (arrowPos == std::string::npos) continue;

        std::string pattern = trim(line.substr(0, arrowPos));
        std::string result = trim(line.substr(arrowPos + 2));

        transformationRules_.emplace_back(pattern, result);
    }
    file.close();
}

void Markov::displayRules() const {
    for (const auto& rule : transformationRules_) {
        std::cout << rule.getPattern() << " -> " << rule.getResult() << std::endl;
    }
}

const std::string& Markov::getCurrentString() const noexcept {
    return currentString_;
}

void Markov::setStartString(const std::string& start) {
    currentString_ = start;
}

bool Markov::applySingleStep() {
    return applyFirstMatchingRule();
}

bool Markov::applyFirstMatchingRule() {
    for (auto& rule : transformationRules_) {
        size_t pos = currentString_.find(rule.getPattern());
        if (pos != std::string::npos) {
            currentString_.replace(pos, rule.getPattern().length(), rule.getResult());
            return true;
        }
    }
    return false;
}
