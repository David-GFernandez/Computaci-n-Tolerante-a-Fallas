#include <iostream>
#include <vector>
#include <cassert>

double obtenerElemento(const std::vector<double>& vec, int indice) {
    // Verificar que el �ndice est� dentro del rango v�lido del vector
    assert(indice >= 0 && indice < vec.size());

    return vec[indice];
}

int main() {
    std::vector<double> datos = {10.5, 15.4, 20.3, 25.2, 30.1};
    int indice = 0;

    std::cout << "Ingrese indice (0-4): ";
    std::cin >> indice;
    std::cout << std::endl;

    // Intentar obtener el elemento en el �ndice especificado

    double elemento = obtenerElemento(datos, indice);
    //double elemento = datos[indice];
    std::cout << "Elemento en el indice " << indice << ": " << elemento << std::endl;

    return 0;
}
