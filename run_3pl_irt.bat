@echo off
call activate
call conda activate %1
py-irt.exe train 3pl %2 %3 --device=cuda --epochs=5000 1> NUL
cat %3\best_parameters.json
