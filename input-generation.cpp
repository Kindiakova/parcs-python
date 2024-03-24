#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime>

std::string generateRandomString(int length) {
    const std::string charset = "abcdefghijklmnopqrstuvwxyz";
    std::string result;
    result.reserve(length);
    srand(static_cast<unsigned int>(time(nullptr)));
    for (int i = 0; i < length; ++i) {
        result += charset[rand() % charset.length()];
    }
    return result;
}

int main() {
    int length = 30000000;
    std::string randomString = generateRandomString(length);

    std::ofstream outputFile("output.txt");
    if (outputFile.is_open()) {
        outputFile << randomString;
        outputFile.close();
        std::cout << "String has been written to output.txt successfully." << std::endl;
    } else {
        std::cerr << "Error opening the file." << std::endl;
        return 1;
    }

    return 0;
}
