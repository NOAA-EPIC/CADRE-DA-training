# Quick Start Guide

1. Clone this repository:
```
git clone https://github.com/chan-hoo/cadre26_noaa_tutorial
```

2. Check JEDI input YAML files and modify them as needed:
```
cd input_yaml
```
- Day1:
```
cp Day1/jedi_3dvar* .
vim jedi_3dvar_fv3_2024022400.yaml
vim jedi_3dvar_fv3inc_2024022400.yaml
```
- Day2:
```
cp Day2/jedi_3dvar* .
```
- Day3:
```
cp Day3/jedi_3dvar* .
sed '399r Day3/obs_[option].yaml' jedi_3dvar_fv3_template.yaml > jedi_3dvar_fv3_2024022400.yaml
vim jedi_3dvar_fv3_2024022400.yaml
```

3. Open job-card script:
```
cd ..
vim run_3dvar_[platform].sh
```
where `[platform]` is `ursa`, `hercules`, or `orion`.

4. Check account (project) name and change it:

5. Submit job-card script:
```
sbatch run_3dvar_[platform].sh
```

6. Check log file:
```
vim log.cadre26.[job_id]
```

7. Move to experimental case directory:
```
cd exp_case/cadre26.[job_id]
```

8. Move to plot directory:
```
cd plot
```

9. Load python environment:
```
source load_py_env.[ploatform]
```

10. Check YAML files for plotting:
```
vim plot_[option].yaml
```
where `[option]` is `cubed_sphere_grid`, `hofx_stats`, or `obs_file`.

11. Run plotting scripts:
```
./plot_[option].py
```
