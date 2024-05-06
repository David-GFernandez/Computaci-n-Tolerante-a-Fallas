from prefect import flow, task
import random
from datetime import timedelta

# Función para eliminar números pares de la lista
@task(cache_expiration=timedelta(minutes=2))
def eliminar_pares(datos_a_ordenar):
    # Simulación de fallo aleatorio
    if random.random() < 0.4:  # Probabilidad de fallo del 40%
        raise Exception("Error: Tiempo de eliminación de números pares excedido.")
    return [x for x in datos_a_ordenar if x % 2 != 0]

# Función para eliminar números impares de la lista
@task(cache_expiration=timedelta(minutes=2))
def eliminar_impares(datos_a_ordenar):
    # Simulación de fallo aleatorio
    if random.random() < 0.4:  # Probabilidad de fallo del 40%
        raise Exception("Error: Tiempo de eliminación de números impares excedido.")
    return [x for x in datos_a_ordenar if x % 2 == 0]

# Flujo para eliminar números pares
@flow(name="eliminar_pares", retries=2, retry_delay_seconds=2, log_prints=True)
def flujo_eliminar_pares():
    datos_a_ordenar = [random.randint(1, 500) for _ in range(1000)]
    return eliminar_pares(datos_a_ordenar)

# Flujo para eliminar números impares
@flow(name="eliminar_impares", retries=2, retry_delay_seconds=2, log_prints=True)
def flujo_eliminar_impares():
    datos_a_ordenar = [random.randint(1, 500) for _ in range(1000)]
    return eliminar_impares(datos_a_ordenar)

if __name__ == "__main__":
    flujo_eliminar_pares()
    flujo_eliminar_impares()