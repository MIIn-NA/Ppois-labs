#include <UnitTest++.h>
#include "Set.h"
#include <sstream>

TEST(EmptySetBasics) {
    Set s;
    CHECK_EQUAL(0u, s.size());
    CHECK(s.isEmpty());
}

TEST(AddUniqueness) {
    Set s;
    CHECK(s.add(SetElement(1)));
    CHECK(!s.add(SetElement(1)));
    CHECK_EQUAL(1u, s.size());
}

TEST(StringElement) {
    Set s;
    CHECK(s.add(SetElement(std::string("bee"))));
    CHECK(s.contains(SetElement(std::string("bee"))));
}

TEST(NestedSetSimple) {
    Set inner;
    inner.add(SetElement(3));
    Set s;
    CHECK(s.add(SetElement(inner)));
    CHECK(s.contains(SetElement(inner)));
}

TEST(EqualityNested) {
    Set a;
    Set inner; inner.add(SetElement(1));
    a.add(SetElement(inner));
    Set b;
    Set inner2; inner2.add(SetElement(1));
    b.add(SetElement(inner2));
    CHECK(a == b);
}

TEST(InequalityDifferent) {
    Set a; a.add(SetElement(1));
    Set b; b.add(SetElement(2));
    CHECK(a != b);
}

TEST(RemoveElement) {
    Set s;
    s.add(SetElement(1));
    CHECK(s.remove(SetElement(1)));
    CHECK(!s.contains(SetElement(1)));
}

TEST(UnionBasic) {
    Set a; a.add(SetElement(1));
    Set b; b.add(SetElement(2));
    auto u = Set::unionWith(a, b);
    CHECK(u.contains(SetElement(1)));
    CHECK(u.contains(SetElement(2)));
    CHECK_EQUAL(2u, u.size());
}

TEST(IntersectionBasic) {
    Set a; a.add(SetElement(1)); a.add(SetElement(2));
    Set b; b.add(SetElement(2)); b.add(SetElement(3));
    auto it = Set::intersectionWith(a, b);
    CHECK(it.contains(SetElement(2)));
    CHECK_EQUAL(1u, it.size());
}

TEST(DifferenceBasic) {
    Set a; a.add(SetElement(1)); a.add(SetElement(2));
    Set b; b.add(SetElement(2));
    auto d = Set::differenceWith(a, b);
    CHECK(d.contains(SetElement(1)));
    CHECK(!d.contains(SetElement(2)));
    CHECK_EQUAL(1u, d.size());
}

TEST(SubSetTrue) {
    Set a; a.add(SetElement(1));
    Set b; b.add(SetElement(1)); b.add(SetElement(2));
    CHECK(a.subsetOf(b));
}

TEST(SubSetFalse) {
    Set a; a.add(SetElement(2));
    Set b; b.add(SetElement(1));
    CHECK(!a.subsetOf(b));
}

TEST(SerializeFlat) {
    Set s; s.add(SetElement(1)); s.add(SetElement(2));
    auto out = s.toString();
    CHECK(out.find("1") != std::string::npos);
    CHECK(out.find("2") != std::string::npos);
}

TEST(SerializeNested) {
    Set inner; inner.add(SetElement(3));
    Set s; s.add(SetElement(1)); s.add(SetElement(inner));
    auto out = s.toString();
    CHECK(out.find("{") != std::string::npos);
    CHECK(out.find("}") != std::string::npos);
}

TEST(ParseEmpty) {
    auto s = Set::fromString("{ }");
    CHECK_EQUAL(0u, s.size());
}

TEST(ParseNumbers) {
    auto s = Set::fromString("{1, 2, 3}");
    CHECK_EQUAL(3u, s.size());
    CHECK(s.contains(SetElement(2)));
}

TEST(ParseStrings) {
    auto s = Set::fromString("{\"a\", \"b\"}");
    CHECK(s.contains(SetElement(std::string("a"))));
}

TEST(ParseNested) {
    auto s = Set::fromString("{1, {2, 3}}");
    Set inner; inner.add(SetElement(2)); inner.add(SetElement(3));
    CHECK(s.contains(SetElement(inner)));
}

TEST(IOStreamExtraction) {
    std::istringstream iss("{1, 2, {3}}\n");
    Set s; iss >> s;
    CHECK(s.contains(SetElement(1)));
    CHECK(s.contains(SetElement(Set::fromString("{3}"))));
}

TEST(CopyConstructor) {
    Set a; a.add(SetElement(1));
    Set b(a);
    CHECK(b.contains(SetElement(1)));
    CHECK(a == b);
}

TEST(AssignmentOperator) {
    Set a; a.add(SetElement(1));
    Set b; b = a;
    CHECK(b.contains(SetElement(1)));
    CHECK(a == b);
}

TEST(RemoveMissing) {
    Set s; s.add(SetElement(1));
    CHECK(!s.remove(SetElement(2)));
    CHECK_EQUAL(1u, s.size());
}

TEST(UnionWithDuplicates) {
    Set a; a.add(SetElement(1));
    Set b; b.add(SetElement(1)); b.add(SetElement(2));
    auto u = Set::unionWith(a, b);
    CHECK_EQUAL(2u, u.size());
}

TEST(IntersectionNone) {
    Set a; a.add(SetElement(1));
    Set b; b.add(SetElement(2));
    auto it = Set::intersectionWith(a, b);
    CHECK_EQUAL(0u, it.size());
}

TEST(DifferenceAll) {
    Set a; a.add(SetElement(1));
    Set b; b.add(SetElement(1));
    auto d = Set::differenceWith(a, b);
    CHECK_EQUAL(0u, d.size());
}

TEST(DeepNestedEquality) {
    Set inner; inner.add(SetElement(1));
    Set deep; deep.add(SetElement(inner));
    Set a1; a1.add(SetElement(deep));
    Set a2; a2.add(SetElement(Set(deep)));
    CHECK(a1 == a2);
}

TEST(SubsetNestedTrue) {
    auto a = Set::fromString("{{1,2}, 3}");
    auto b = Set::fromString("{{1,2}, 3, 4}");
    CHECK(a.subsetOf(b));
}

TEST(SubsetNestedFalse) {
    auto a = Set::fromString("{{1,2}}");
    auto b = Set::fromString("{{2,3}}");
    CHECK(!a.subsetOf(b));
}

TEST(ParseNegativeNumbers) {
    auto s = Set::fromString("{-1, 2}");
    CHECK(s.contains(SetElement(-1)));
    CHECK(s.contains(SetElement(2)));
}

TEST(SerializeQuotesForStrings) {
    auto s = Set::fromString("{\"bee\"}");
    CHECK_EQUAL("{\"bee\"}", s.toString());
}

TEST(NormalizeOrderStable) {
    auto s = Set::fromString("{\"b\", \"a\", 2, 1}");
    auto out = s.toString();
    CHECK(out.find("1") < out.find("2"));
}

int main() {
    return UnitTest::RunAllTests();
}
