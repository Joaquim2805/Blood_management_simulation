# **Blood Management Simulation**

## **Description**

This project models a two-stage stochastic optimization problem for blood collection and inventory management. The objective is to meet a hospital’s dynamic blood demand while minimizing logistics costs, considering the perishability of blood and uncertainties in demand and availability.

---

## **Core Objectives**

### **Two-Stage Decision Process**

1. **First Stage**: Plan vehicle routes and initial collection based on forecasted demand and availability.
2. **Second Stage**: Adjust for realized demand through emergency collections if needed.

### **Cost Optimization**

- Minimize transportation costs.
- Reduce wastage due to blood expiration.

### **Dynamic Stock Management**

- Track blood inventory daily.
- Account for consumption and remove expired stock after three weeks.

---

## **Key Features**

- **Modelization with Gurobi**: Solve vehicle routing and blood collection problems with capacity and demand constraints.
- **Stochastic Simulations**: Model uncertainty in hospital demand and center availability.
- **Perishability Integration**: Automatically update and remove expired blood from inventory.

---

## **Technologies and Libraries**

- **Python**: Programming and simulation.
- **Gurobi**: MILP solver for optimization.
- **NumPy**: Numerical computations for data handling.

---

### **Usage**

Clone the repository and follow the instructions to set up the environment and run simulations. Ensure that Gurobi is correctly installed and licensed.

```bash
git clone https://github.com/Joaquim2805/Blood_management_simulation.git
cd Blood_management_simulation
pip install -r requirements.txt

```
