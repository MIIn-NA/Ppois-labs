#pragma once

#include <string>


class Rule {
public:
  
    Rule();

  
    Rule(const std::string& pattern, const std::string& result);


    bool operator==(const Rule& other) const;

 
    const std::string& getPattern() const noexcept;
    const std::string& getResult() const noexcept;

private:
    std::string pattern_;
    std::string result_;
};
