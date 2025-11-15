#include <gtest/gtest.h>
#include "Set.h"
#include <sstream>

class SetTest : public ::testing::Test {
protected:
    void SetUp() override {
        emptySet = Set();
        simpleSet = Set("{a, b, c}");
        simpleSetTwo = Set("{d, c, a, e}");
        nestedSet = Set("{{x, y}, z}");
        nestedSetTwo = Set("{x, y, {}, {x, y}, z}");
    }

    Set emptySet, simpleSet, simpleSetTwo, nestedSet, nestedSetTwo;
};

// --- Конструкторы и базовые свойства ---
TEST_F(SetTest, DefaultConstructor) {
    EXPECT_TRUE(emptySet.isEmpty());
    EXPECT_EQ(emptySet.size(), 0);
    EXPECT_EQ(emptySet.serialize(), "{}");
}

TEST_F(SetTest, FromEmptyString) {
    Set set("{}");
    EXPECT_TRUE(set.isEmpty());
    EXPECT_EQ(set.size(), 0);
}

TEST_F(SetTest, FromStringSimple) {
    EXPECT_FALSE(simpleSet.isEmpty());
    EXPECT_EQ(simpleSet.size(), 3);
    EXPECT_TRUE(simpleSet.has(Set::Element("a")));
    EXPECT_TRUE(simpleSet.has(Set::Element("b")));
    EXPECT_TRUE(simpleSet.has(Set::Element("c")));
    EXPECT_FALSE(simpleSet.has(Set::Element("d")));
}

TEST_F(SetTest, FromStringNested) {
    EXPECT_EQ(nestedSet.size(), 2);
    Set::Element inner({Set::Element("x"), Set::Element("y")});
    EXPECT_TRUE(nestedSet.has(inner));
    EXPECT_TRUE(nestedSet.has(Set::Element("z")));
}

TEST_F(SetTest, CopyConstructor) {
    Set copy(simpleSet);
    EXPECT_EQ(copy, simpleSet);
    EXPECT_EQ(copy.size(), simpleSet.size());
}

TEST_F(SetTest, AssignmentOperator) {
    Set A("{a, b}");
    Set B("{x, y, z}");
    B = A;
    EXPECT_EQ(A, B);
    EXPECT_EQ(B.size(), 2);
}

TEST_F(SetTest, SelfAssignment) {
    Set set("{1, 2, 3}");
    set = set;
    EXPECT_EQ(set.size(), 3);
}

// --- Методы добавления/удаления ---
TEST_F(SetTest, InsertElement) {
    Set set = emptySet;
    set.insert(Set::Element("test"));
    EXPECT_EQ(set.size(), 1);
    EXPECT_TRUE(set.has(Set::Element("test")));
}

TEST_F(SetTest, InsertNestedElement) {
    Set set = nestedSet;
    Set::Element inner({Set::Element("test1"), Set::Element("test2")});
    set.insert(inner);
    EXPECT_EQ(set.size(), 3);
    EXPECT_TRUE(set.has(inner));
}

TEST_F(SetTest, InsertDuplicate) {
    Set set = simpleSet;
    size_t initial = set.size();
    set.insert(Set::Element("a"));
    EXPECT_EQ(set.size(), initial);
}

TEST_F(SetTest, InsertDuplicateNested) {
    Set set = nestedSet;
    size_t initial = set.size();
    Set::Element inner({Set::Element("x"), Set::Element("y")});
    set.insert(inner);
    EXPECT_EQ(set.size(), initial);
}

TEST_F(SetTest, EraseElement) {
    Set set = simpleSet;
    set.erase(Set::Element("b"));
    EXPECT_EQ(set.size(), 2);
    EXPECT_FALSE(set.has(Set::Element("b")));
    EXPECT_TRUE(set.has(Set::Element("a")));
    EXPECT_TRUE(set.has(Set::Element("c")));
}

TEST_F(SetTest, EraseNestedElement) {
    Set set = nestedSet;
    Set::Element inner({Set::Element("x"), Set::Element("y")});
    set.erase(inner);
    EXPECT_EQ(set.size(), 1);
}

TEST_F(SetTest, EraseNonExistent) {
    Set set = simpleSet;
    size_t initial = set.size();
    set.erase(Set::Element("x"));
    EXPECT_EQ(set.size(), initial);
}

// --- Операции над множествами ---
TEST_F(SetTest, Unite) {
    Set result = simpleSet.unite(simpleSetTwo);
    EXPECT_EQ(result.size(), 5);
    EXPECT_TRUE(result.has(Set::Element("a")));
    EXPECT_TRUE(result.has(Set::Element("b")));
    EXPECT_TRUE(result.has(Set::Element("c")));
    EXPECT_TRUE(result.has(Set::Element("d")));
    EXPECT_TRUE(result.has(Set::Element("e")));
}

TEST_F(SetTest, Intersect) {
    Set result = simpleSet.intersect(simpleSetTwo);
    EXPECT_EQ(result.size(), 2);
    EXPECT_TRUE(result.has(Set::Element("a")));
    EXPECT_TRUE(result.has(Set::Element("c")));
    EXPECT_FALSE(result.has(Set::Element("b")));
}

TEST_F(SetTest, Difference) {
    Set result = simpleSetTwo.difference(simpleSet);
    EXPECT_EQ(result.size(), 2);
    EXPECT_TRUE(result.has(Set::Element("d")));
    EXPECT_TRUE(result.has(Set::Element("e")));
    EXPECT_FALSE(result.has(Set::Element("a")));
}

TEST_F(SetTest, SelfUnite) {
    simpleSet.selfUnite(simpleSetTwo);
    EXPECT_EQ(simpleSet.size(), 5);
    EXPECT_TRUE(simpleSet.has(Set::Element("d")));
    EXPECT_TRUE(simpleSet.has(Set::Element("e")));
}

TEST_F(SetTest, SelfIntersect) {
    simpleSet.selfIntersect(simpleSetTwo);
    EXPECT_EQ(simpleSet.size(), 2);
    EXPECT_TRUE(simpleSet.has(Set::Element("a")));
    EXPECT_TRUE(simpleSet.has(Set::Element("c")));
}

TEST_F(SetTest, SelfDifference) {
    simpleSetTwo.selfDifference(simpleSet);
    EXPECT_EQ(simpleSetTwo.size(), 2);
    EXPECT_TRUE(simpleSetTwo.has(Set::Element("d")));
    EXPECT_TRUE(simpleSetTwo.has(Set::Element("e")));
}

TEST_F(SetTest, HasMethod) {
    Set set("{p, q}");
    EXPECT_TRUE(set.has(Set::Element("p")));
    EXPECT_FALSE(set.has(Set::Element("r")));
}

TEST_F(SetTest, SerializeEmpty) {
    Set set;
    EXPECT_EQ(set.serialize(), "{}");
}

// --- Отдельные тестовые наборы ---

class SetConstructorTest : public ::testing::Test {};

TEST(SetConstructorTest, FromEmptyString) {
    Set set("{}");
    EXPECT_TRUE(set.isEmpty());
    EXPECT_EQ(set.size(), 0);
}

class SetPowerSetTest : public ::testing::Test {};

TEST(SetPowerSetTest, Empty) {
    Set empty;
    Set power = empty.powerSet();
    EXPECT_EQ(power.size(), 1);
    EXPECT_TRUE(power.has(Set::Element(std::vector<Set::Element>())));
}

TEST(SetPowerSetTest, Singleton) {
    Set single("{a}");
    Set power = single.powerSet();
    EXPECT_EQ(power.size(), 2);
    EXPECT_TRUE(power.has(Set::Element(std::vector<Set::Element>())));
    EXPECT_TRUE(power.has(Set::Element(std::vector<Set::Element>{Set::Element("a")})));
}

TEST(SetPowerSetTest, TwoElements) {
    Set set("{1, 2}");
    Set power = set.powerSet();
    EXPECT_EQ(power.size(), 4);
    EXPECT_TRUE(power.has(Set::Element(std::vector<Set::Element>())));
    EXPECT_TRUE(power.has(Set::Element(std::vector<Set::Element>{Set::Element("1")})));
    EXPECT_TRUE(power.has(Set::Element(std::vector<Set::Element>{Set::Element("2")})));
    EXPECT_TRUE(power.has(Set::Element(std::vector<Set::Element>{Set::Element("1"), Set::Element("2")})));
}

TEST(SetPowerSetTest, ThreeElements) {
    Set set("{x, y, z}");
    Set power = set.powerSet();
    EXPECT_EQ(power.size(), 8);
}

class SetParsingTest : public ::testing::Test {};

TEST(SetParsingTest, InvalidFormat) {
    EXPECT_THROW(Set("{a, b"), std::invalid_argument);
    EXPECT_THROW(Set("a, b}"), std::invalid_argument);
    EXPECT_THROW(Set(""), std::invalid_argument);
    EXPECT_THROW(Set("abc"), std::invalid_argument);
}

TEST(SetParsingTest, InvalidCharacters) {
    EXPECT_THROW(Set("{a, b@c}"), std::invalid_argument);
    EXPECT_THROW(Set("{a, b!c}"), std::invalid_argument);
}

TEST(SetParsingTest, UnexpectedBrace) {
    EXPECT_THROW(Set("{a, b{c}"), std::invalid_argument);
}

class SetComplexTest : public ::testing::Test {};

TEST(SetComplexTest, DeepNesting) {
    Set complex("{{{a, b}}, {c, {d, e}}}");
    EXPECT_EQ(complex.size(), 2);
    std::string s = complex.serialize();
    EXPECT_NE(s.find("a"), std::string::npos);
    EXPECT_NE(s.find("e"), std::string::npos);
}

TEST(SetComplexTest, ContainsEmptySet) {
    Set set("{ {}, a }");
    EXPECT_TRUE(set.has(Set::Element(std::vector<Set::Element>())));
    EXPECT_TRUE(set.has(Set::Element("a")));
}

class ElementTest : public ::testing::Test {};

TEST(ElementTest, DefaultConstructor) {
    Set::Element e;
    EXPECT_EQ(e.type, Set::VALUE);
}

TEST(ElementTest, StringConstructor) {
    Set::Element e("hello");
    EXPECT_EQ(e.atom, "hello");
}

TEST(ElementTest, NestedConstructor) {
    Set::Element e({Set::Element("x"), Set::Element("y")});
    EXPECT_EQ(e.subset.size(), 2);
}

TEST(ElementTest, Equality) {
    Set::Element a("x");
    Set::Element b("x");
    Set::Element c("y");
    EXPECT_TRUE(a == b);
    EXPECT_FALSE(a == c);
}

class SetDeserializeTest : public ::testing::Test {};

TEST(SetDeserializeTest, RoundTrip) {
    std::string input = "{a, {b, c}, d}";
    Set set = Set::deserialize(input);
    EXPECT_EQ(set.serialize(), input);
}

// --- Потоковые операторы ---
TEST_F(SetTest, StreamOutput) {
    std::stringstream ss;
    ss << simpleSet;
    std::string result = ss.str();
    EXPECT_NE(result.find("a"), std::string::npos);
    EXPECT_EQ(result.front(), '{');
    EXPECT_EQ(result.back(), '}');
}

TEST_F(SetTest, StreamInput) {
    std::stringstream ss("{{a, b}, c}");
    Set set;
    ss >> set;
    EXPECT_EQ(set.size(), 2);
    Set::Element inner({Set::Element("a"), Set::Element("b")});
    EXPECT_TRUE(set.has(inner));
    EXPECT_TRUE(set.has(Set::Element("c")));
}

// --- Главная функция ---
int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
