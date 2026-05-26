# ONNX2FPGA

Open-source research repository for exploring end-to-end flows from trained neural networks to FPGA-ready implementations. The workspace includes model training artifacts, ONNX exports, HLS/Vitis AI flows, and supporting notebooks for multiple space-focused use cases.

## Highlights
- Multiple networks and datasets (CNet, ESPERTA, MMSNet, VAENet).
- ONNX conversion and processing utilities.
- HLS and AMD DPU with Vitis AI, plus PYNQ integration.
- Reproducible notebooks and scripts for model export and hardware builds.

## Repository layout
- Common: training and ONNX artifacts per network
- FINN: FINN flow notebooks and helper scripts (WIP)
- HLS: C code generation and HLS projects
- HLS4ML: hls4ml conversions and notebooks (WIP)
- PYNQ: board-level workflows and experiments
- VitisAI: AMD DPU integration with Vitis AI
- onnx2c: ONNX to C conversion tooling

## Setup
### Python virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install onnx onnxscript onnxruntime torch torchvision matplotlib brevitas
pip install requests pandas spacepy
```

### Alternative: install from requirements
```bash
pip install -r requirements.txt
```

## Useful commands
- rsync -r <source_dir> <dest_dir>

## How to use
Most workflows are driven by notebooks and scripts inside each subfolder. A typical flow is:
1. Train or load a model in Common.
2. Export to ONNX.
3. Convert to C or HLS using HLS or onnx2c.
4. Run board-level experiments in PYNQ or VitisAI.

## Citation
If you use this repository, please cite:
```
@INPROCEEDINGS{11310891,
  author={Antunes, Pedro and Al Hafiz, Muhammad Ihsan and Ekelund, Jonah and Dineva, Ekaterina and Miloshevich, George and Gonidakis, Panagiotis and Podobas, Artur},
  booktitle={2025 IEEE 18th International Symposium on Embedded Multicore/Many-core Systems-on-Chip (MCSoC)},
  title={Evaluating Four FPGA-Accelerated Space Use Cases Based on Neural Network Algorithms for On-Board Inference},
  year={2025},
  volume={},
  number={},
  pages={804-812},
  keywords={Space vehicles;Three-dimensional displays;Quantization (signal);Power demand;Filtering;Space missions;Artificial neural networks;Inference algorithms;Artificial intelligence;Field programmable gate arrays;FPGA;Neural Network;HLS;Vitis AI;Space Mission},
  doi={10.1109/MCSoC67473.2025.00126}}
```

## References
### Jonah Ekelund et al. Paper
```
@article{ekelund2024ai,
  title={AI in Space for Scientific Missions: Strategies for Minimizing Neural-Network Model Upload},
  author={Ekelund, Jonah and Vinuesa, Ricardo and Khotyaintsev, Yuri and Henri, Pierre and Delzanno, Gian Luca and Markidis, Stefano},
  journal={arXiv preprint arXiv:2406.14297},
  year={2024}
}
```

### Vyacheslav Olshevsky Work
#### Olshevsky et al. Paper
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
  author={Olshevsky, Vyacheslav and Khotyaintsev, Yuri V. and Lalti, Ahmad and Divin, Andrey and Delzanno, Gian Luca and Anderzen, Sven and Herman, Pawel and Chien, Steven W. D. and Avanov, Levon and Dimmock, Andrew P. and Markidis, Stefano},
  year={2021},
  month=sep
}
```

#### Git Repository
https://bitbucket.org/volshevsky/mmslearning/