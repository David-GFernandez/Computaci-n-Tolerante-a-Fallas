#include <iostream>
#include <vector>
#include <cassert>

#include <iostream>
#include <vector>

double obtenerElemento(const std::vector<double>& vec, int indice) {
    // Verificar que el índice esté dentro del rango válido del vector
    if (indice < 0 || indice >= vec.size()) {
        throw std::out_of_range("Índice fuera de rango");
    }

    return vec[indice];
}

int main() {
    std::vector<double> datos = {10.5, 15.4, 20.3, 25.2, 30.1};
    int indice = 0;

    std::cout << "Ingrese indice (0-4): ";
    std::cin >> indice;
    std::cout << std::endl;

    // Intentar obtener el elemento en el índice especificado
    try {
        double elemento = obtenerElemento(datos, indice);
        std::cout << "Elemento en el indice " << indice << ": " << elemento << std::endl;
    } catch (const std::out_of_range& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
