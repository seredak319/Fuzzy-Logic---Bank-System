# Fuzzy Banker

A command-line Fuzzy Inference System (FIS) for supporting bank loan decisions using both Type-1 (Mamdani) and Type-2 (Larsen + centroid) defuzzification.  

## Features

- **Fuzzification** of input criteria (inflow, income_sum, dependents, age) against user-configurable membership functions.  
- **Rule-based inference** in both Type-1 and Type-2 fuzzy logic.  
- **Defuzzification** with:
  - **Type-1**: Mamdani “reverse mapping” (analytical inverse of monotonic MFs → centroid).  
  - **Type-2**: Larsen scaling + aggregated centroid (piecewise rectangles & trapezoids or numerical trapz).  
- **Modular architecture**:
  - `controller/`: CLI parsing & config loading.  
  - `method/`: Fuzzifier, InferenceEngine, DefuzzifierType1, DefuzzifierType2.  
  - `model/`: Problem definition (decision rules).  
  - `logger/`: Logging of inputs, membership degrees, intermediate & final results.  
- **Plain-text interface**, no GUI, runs on any standard Python environment.