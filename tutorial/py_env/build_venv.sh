module purge
module load python
rm -rf cadre_pyenv
python3 -m venv cadre_pyenv
source cadre_pyenv/bin/activate
pip install --upgrade pip
pip install -r cadre_env_list.txt
pip list
