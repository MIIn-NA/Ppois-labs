#include <gtest/gtest.h>
#include <fstream>
#include <filesystem>
#include "Rule.h"
#include "Markov.h"

TEST(RuleTest, DefaultConstructor) {
    Rule r;
    EXPECT_EQ(r.getPattern(), "");
    EXPECT_EQ(r.getResult(), "");
}

TEST(RuleTest, ParameterizedConstructor) {
    Rule r("abc", "xyz");
    EXPECT_EQ(r.getPattern(), "abc");
    EXPECT_EQ(r.getResult(), "xyz");
}

TEST(RuleTest, EqualityOperator_Equal) {
    Rule r1("a", "b");
    Rule r2("a", "b");
    EXPECT_TRUE(r1 == r2);
}

TEST(RuleTest, EqualityOperator_NotEqual_Pattern) {
    Rule r1("a", "b");
    Rule r2("x", "b");
    EXPECT_FALSE(r1 == r2);
}

TEST(RuleTest, EqualityOperator_NotEqual_Result) {
    Rule r1("a", "b");
    Rule r2("a", "y");
    EXPECT_FALSE(r1 == r2);
}

TEST(MarkovTest, DefaultConstructor) {
    Markov m;
    EXPECT_EQ(m.getCurrentString(), "");
}

TEST(MarkovTest, SetAndGetStartString) {
    Markov m;
    m.setStartString("initial");
    EXPECT_EQ(m.getCurrentString(), "initial");
}

TEST(MarkovTest, AddTransformationRule_Single) {
    Markov m;
    m.addTransformationRule("ab", "cd");
    m.setStartString("ab");
    EXPECT_TRUE(m.applySingleStep());
    EXPECT_EQ(m.getCurrentString(), "cd");
}

TEST(MarkovTest, AddTransformationRule_DuplicateIgnored) {
    Markov m;
    m.addTransformationRule("x", "y");
    m.addTransformationRule("x", "y");
    m.setStartString("x");
    EXPECT_TRUE(m.applySingleStep());
    EXPECT_EQ(m.getCurrentString(), "y");
    EXPECT_FALSE(m.applySingleStep());
}

TEST(MarkovTest, RemoveTransformationRule_Existing) {
    Markov m;
    m.addTransformationRule("to_remove", "z");
    EXPECT_TRUE(m.removeTransformationRule("to_remove", "z"));
    m.setStartString("to_remove");
    EXPECT_FALSE(m.applySingleStep());
}

TEST(MarkovTest, RemoveTransformationRule_NonExisting) {
    Markov m;
    EXPECT_FALSE(m.removeTransformationRule("nonexistent", "value"));
}

TEST(MarkovTest, ModifyRuleAt_ValidIndex) {
    Markov m;
    m.addTransformationRule("old", "val");
    EXPECT_TRUE(m.modifyRuleAt(0, "new", "replaced"));
    m.setStartString("new");
    EXPECT_TRUE(m.applySingleStep());
    EXPECT_EQ(m.getCurrentString(), "replaced");
}

TEST(MarkovTest, ModifyRuleAt_EmptyRules) {
    Markov m;
    EXPECT_FALSE(m.modifyRuleAt(0, "a", "b"));
}

TEST(MarkovTest, ModifyRuleAt_IndexOutOfRange) {
    Markov m;
    m.addTransformationRule("x", "y");
    EXPECT_FALSE(m.modifyRuleAt(1, "a", "b"));
    EXPECT_FALSE(m.modifyRuleAt(100, "a", "b"));
}

TEST(MarkovTest, ApplySingleStep_NoMatch) {
    Markov m;
    m.addTransformationRule("not_found", "x");
    m.setStartString("hello");
    EXPECT_FALSE(m.applySingleStep());
    EXPECT_EQ(m.getCurrentString(), "hello");
}

TEST(MarkovTest, Execute_FullAlgorithm_Simple) {
    Markov m;
    m.addTransformationRule("aa", "b");
    m.setStartString("aaaa");
    m.execute(false);
    EXPECT_EQ(m.getCurrentString(), "bb");
}

TEST(MarkovTest, Execute_NoRules) {
    Markov m;
    m.setStartString("unchanged");
    m.execute(false);
    EXPECT_EQ(m.getCurrentString(), "unchanged");
}

TEST(MarkovTest, Execute_WithLoggingDoesNotCrash) {
    Markov m;
    m.addTransformationRule("1", "2");
    m.setStartString("111");
    m.execute(true);
    EXPECT_EQ(m.getCurrentString(), "222");
}

TEST(MarkovTest, LoadRulesFromFile_ValidFile) {
    const std::string filename = "test_valid_rules.txt";
    std::ofstream file(filename);
    file << "start\n";
    file << "a -> b\n";
    file << "bb -> c\n";
    file.close();

    Markov m(filename);
    EXPECT_EQ(m.getCurrentString(), "start");
    m.setStartString("aa");
    m.execute(false);
    EXPECT_EQ(m.getCurrentString(), "c");

    std::filesystem::remove(filename);
}

TEST(MarkovTest, LoadRulesFromFile_FileNotFound) {
    Markov m("non_existent_file_12345.txt");
    EXPECT_EQ(m.getCurrentString(), "");
}
TEST(MarkovTest, LoadRulesFromFile_EmptyLinesAndSpaces) {
    const std::string filename = "test_spaces_rules.txt";
    std::ofstream file(filename);
    file << " x \n";  // ← с пробелами!
    file << "  x  ->  y  \n";
    file << "\n";
    file << "y -> z\n";
    file.close();

    Markov m(filename);
    EXPECT_EQ(m.getCurrentString(), "x"); // пробелы удалены
    m.execute(false);
    EXPECT_EQ(m.getCurrentString(), "z"); // x → y → z

    std::filesystem::remove(filename);
}

TEST(MarkovTest, DisplayRules_CapturesOutput) {
    Markov m;
    m.addTransformationRule("p1", "r1");
    m.addTransformationRule("p2", "r2");

    testing::internal::CaptureStdout();
    m.displayRules();
    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_NE(output.find("p1 -> r1"), std::string::npos);
    EXPECT_NE(output.find("p2 -> r2"), std::string::npos);
}

TEST(MarkovTest, ApplyFirstMatchingRule_StopsAtFirstMatch) {
    Markov m;
    m.addTransformationRule("a", "X");
    m.addTransformationRule("a", "Y");
    m.setStartString("a");
    m.applySingleStep();
    EXPECT_EQ(m.getCurrentString(), "X");
}
