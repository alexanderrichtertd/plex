



:: this absolute path (ends with \)
set SELF_PATH=%~dp0

python -c "from data import setEnv; setEnv.SetEnv()"
python -c "from utilities import arStartup; arStartup.start()"

