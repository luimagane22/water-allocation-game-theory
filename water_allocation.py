import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

# Parámetros para evitar divisiones por cero
epsilon = 1e-6
delta = 1e-6

# Función para calcular los pesos de prioridad basados en demandas y sostenibilidad
def compute_priority_weights(claims, sustainability, alpha=1, beta=1):
    return (alpha / (claims + epsilon)) * (beta / (sustainability + delta))

# Método ajustado de asignación basada en prioridades
def priority_allocation_adjusted(claims, sustainability, total_water):
    remaining_water = total_water
    allocations = np.zeros_like(claims)
    remaining_claims = claims.copy()
    
    while remaining_water > 0:
        # Calcular los pesos solo para los agricultores con demandas pendientes
        active_indices = remaining_claims > 0
        weights = compute_priority_weights(remaining_claims[active_indices], sustainability[active_indices])
        normalized_weights = weights / np.sum(weights)
        
        # Distribuir el agua proporcionalmente a los pesos
        distributed_water = normalized_weights * remaining_water
        allocations_to_add = np.minimum(distributed_water, remaining_claims[active_indices])
        
        # Actualizar las asignaciones y las demandas restantes
        allocations[active_indices] += allocations_to_add
        remaining_claims[active_indices] -= allocations_to_add
        remaining_water -= np.sum(allocations_to_add)
        
        # Detener si no queda agua o todas las demandas han sido satisfechas
        if np.sum(remaining_claims[active_indices]) == 0:
            break
    
    return allocations

# Asignación proporcional
def proportional_allocation(claims, total_water):
    return total_water * claims / np.sum(claims)

# Regla de pérdidas iguales restringidas
def constrained_equal_losses(claims, total_water):
    remaining = total_water
    losses = np.zeros_like(claims)
    while remaining > 0:
        losses += 1
        allocations = np.maximum(claims - losses, 0)
        if np.sum(allocations) <= total_water:
            return allocations
    return allocations

# Función para calcular el impacto ambiental
def compute_environmental_impact(allocations, sustainability):
    return np.sum(allocations * sustainability)

# Solicitar datos al usuario con validaciones
while True:
    try:
        num_farmers = int(input("Ingrese el número de agricultores: "))
        if num_farmers <= 0:
            raise ValueError("El número de agricultores debe ser mayor a 0.")
        break
    except ValueError as e:
        print(f"Entrada inválida: {e}. Intente nuevamente.")

claims = []
sustainability = []
for i in range(num_farmers):
    while True:
        try:
            claim = float(input(f"Ingrese la demanda del agricultor {i+1} (en litros): "))
            if claim < 0:
                raise ValueError("Las demandas deben ser números positivos.")
            claims.append(claim)
            break
        except ValueError as e:
            print(f"Entrada inválida: {e}. Intente nuevamente.")

    while True:
        try:
            sustain = float(input(f"Ingrese el índice de sostenibilidad del agricultor {i+1} (entre menor, mejor): "))
            if sustain <= 0:
                raise ValueError("El índice de sostenibilidad debe ser mayor a 0.")
            sustainability.append(sustain)
            break
        except ValueError as e:
            print(f"Entrada inválida: {e}. Intente nuevamente.")

while True:
    try:
        E = float(input("Ingrese la cantidad total de agua disponible (en litros): "))
        if E <= 0:
            raise ValueError("La cantidad total de agua debe ser mayor a 0.")
        break
    except ValueError as e:
        print(f"Entrada inválida: {e}. Intente nuevamente.")

claims = np.array(claims)
sustainability = np.array(sustainability)

# Asignaciones basadas en prioridades con el método ajustado
priority_allocations = priority_allocation_adjusted(claims, sustainability, E)

# Asignaciones proporcionales
proportional_allocations = proportional_allocation(claims, E)

# Asignaciones con pérdidas iguales restringidas
losses_allocations = constrained_equal_losses(claims, E)

# Calcular los impactos ambientales
priority_impact = compute_environmental_impact(priority_allocations, sustainability)
proportional_impact = compute_environmental_impact(proportional_allocations, sustainability)
losses_impact = compute_environmental_impact(losses_allocations, sustainability)

# Exportar resultados a CSV
df = pd.DataFrame({
    'Agricultor': [f'Agricultor {i+1}' for i in range(len(claims))],
    'Demanda': claims,
    'Sostenibilidad': sustainability,
    'Asignaciones por Prioridad': priority_allocations,
    'Asignaciones Proporcionales': proportional_allocations,
    'Asignaciones por Pérdidas Iguales': losses_allocations
})
csv_path = os.path.join(os.getcwd(), 'comparacion_asignaciones.csv')
df.to_csv(csv_path, index=False)

# Visualización interactiva de asignaciones
fig_allocations = go.Figure()
fig_allocations.add_trace(go.Bar(x=[f'Agricultor {i+1}' for i in range(len(claims))], y=claims, name='Demandas'))
fig_allocations.add_trace(go.Bar(x=[f'Agricultor {i+1}' for i in range(len(priority_allocations))], y=priority_allocations, name='Asignaciones por Prioridad'))
fig_allocations.add_trace(go.Bar(x=[f'Agricultor {i+1}' for i in range(len(proportional_allocations))], y=proportional_allocations, name='Asignaciones Proporcionales'))
fig_allocations.add_trace(go.Bar(x=[f'Agricultor {i+1}' for i in range(len(losses_allocations))], y=losses_allocations, name='Asignaciones por Pérdidas Iguales'))

# Configuración de diseño para mejor visualización
fig_allocations.update_layout(
    title='Comparación de Asignaciones',
    xaxis_title='Agricultores',
    yaxis_title='Agua (litros)',
    barmode='group',
    legend_title='Leyenda',
    width=1200,
    height=600,
    xaxis=dict(
        tickangle=45,
        rangeslider=dict(visible=True)
    ),
    font=dict(size=12)
)

# Visualización interactiva de impactos ambientales
impact_methods = ['Prioridad', 'Proporcional', 'Pérdidas']
impact_values = [priority_impact, proportional_impact, losses_impact]

fig_impact = go.Figure(data=[
    go.Bar(x=impact_methods, y=impact_values, marker_color=['blue', 'green', 'orange'])
])

fig_impact.update_layout(
    title='Comparación de Impactos Ambientales',
    xaxis_title='Método de Asignación',
    yaxis_title='Impacto Ambiental (entre menor, mejor)',
    showlegend=False,
    width=800,
    height=500
)

# Mostrar visualizaciones
fig_allocations.show()
fig_impact.show()

# Imprimir impactos
print("Impacto Ambiental:")
print(f"Impacto de Asignación por Prioridad: {priority_impact}")
print(f"Impacto de Asignación Proporcional: {proportional_impact}")
print(f"Impacto de Asignación por Pérdidas Iguales: {losses_impact}")

# Imprimir la ruta del archivo CSV
print(f"Archivo CSV guardado en: {csv_path}")
