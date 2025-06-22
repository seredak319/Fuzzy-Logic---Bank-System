@echo off
set INFLOW=12000
set INCOME_SUM=12000
set DEPENDENTS=0
set AGE=24

echo --------------------------------------------------
echo Running fuzzy_banker.py with parameters:
echo    Inflow       = %INFLOW%
echo    Income_sum   = %INCOME_SUM%
echo    Dependents   = %DEPENDENTS%
echo    Age          = %AGE%
echo --------------------------------------------------

python fuzzy_banker_type2_lib_comparison.py --inflow %INFLOW% --income_sum %INCOME_SUM% --dependents %DEPENDENTS% --age %AGE%

pause