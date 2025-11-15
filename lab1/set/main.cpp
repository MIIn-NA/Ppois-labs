#include <iostream>
#include "Set.h"

int main() {
    std::cout << "Введите множество: ";
    Set A;
    std::cin >> A;
    std::cout << "Вы ввели: " << A << std::endl;
    std::cout << "Мощность: " << A.size() << std::endl;
    return 0;
}
