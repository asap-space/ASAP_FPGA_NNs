# Dependencies
## Pyhton virtual environment
```bash
python3 -m venv pyenv
source pyenv/bin/activate
pip install --upgrade pip # (optional)
pip install onnx onnxscript onnxruntime torch torchvision matplotlib brevitas 
pip install requests pandas spacepy # For data
```

# Useful commands
rsync -r <source_dir> <dest_dir>

# References
## Jonah Ekelund et al. Paper
```
@article{ekelund2024ai,
  title={AI in Space for Scientific Missions: Strategies for Minimizing Neural-Network Model Upload},
  author={Ekelund, Jonah and Vinuesa, Ricardo and Khotyaintsev, Yuri and Henri, Pierre and Delzanno, Gian Luca and Markidis, Stefano},
  journal={arXiv preprint arXiv:2406.14297},
  year={2024}
}
```
## Vyacheslav Olshevsky Work
### Olshevsky et al. Paper
```
@article{Olshevsky_2021,
   title={Automated Classification of Plasma Regions Using 3D Particle Energy Distributions},
   volume={126},
   ISSN={2169-9402},
   url={http://dx.doi.org/10.1029/2021JA029620},
   DOI={10.1029/2021ja029620},
   number={10},
   journal={Journal of Geophysical Research: Space Physics},
   publisher={American Geophysical Union (AGU)},
   author={Olshevsky, Vyacheslav and Khotyaintsev, Yuri V. and Lalti, Ahmad and Divin, Andrey and Delzanno, Gian Luca and Anderzén, Sven and Herman, Pawel and Chien, Steven W. D. and Avanov, Levon and Dimmock, Andrew P. and Markidis, Stefano},
   year={2021},
   month=sep }
```
### Git Repository
`https://bitbucket.org/volshevsky/mmslearning/`