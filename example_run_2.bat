@echo off
set INFLOW=6500
set INCOME_SUM=12000
set DEPENDENTS=3
set AGE=37

echo --------------------------------------------------
echo Running fuzzy_banker.py with parameters:
echo    Inflow       = %INFLOW%
echo    Income_sum   = %INCOME_SUM%
echo    Dependents   = %DEPENDENTS%
echo    Age          = %AGE%
echo --------------------------------------------------

python fuzzy_banker.py --inflow %INFLOW% --income_sum %INCOME_SUM% --dependents %DEPENDENTS% --age %AGE%

pause