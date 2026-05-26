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
### CNetPlusScalar Neural Network
*George Git Repository*
https://github.com/georgemilosh/PyNets
### ESPERTA
```
@article{Alberti_2017,
  doi = {10.3847/1538-4357/aa5cb8},
  url = {https://doi.org/10.3847/1538-4357/aa5cb8},
  year = {2017},
  month = {mar},
  publisher = {The American Astronomical Society},
  volume = {838},
  number = {1},
  pages = {59},
  author = {Alberti, T. and Laurenza, M. and Cliver, E. W. and Storini, M. and Consolini, G. and Lepreti, F.},
  title = {Solar Activity from 2006 to 2014 and Short-term Forecasts of Solar Proton Events Using the ESPERTA Model},
  journal = {The Astrophysical Journal},
  abstract = {To evaluate the solar energetic proton (SEP) forecast model of Laurenza et al., here termed ESPERTA, we computed the input parameters (soft X-ray (SXR) fluence and ∼1 MHz radio fluence) for all ≥M2 SXR flares from 2006 to 2014. This database is outside the 1995–2005 interval on which ESPERTA was developed. To assess the difference in the general level of activity between these two intervals, we compared the occurrence frequencies of SXR flares and SEP events for the first six years of cycles 23 (1996 September–2002 September) and 24 (2008 December–2014 December). We found a reduction of SXR flares and SEP events of 40% and 46%, respectively, in the latter period. Moreover, the numbers of ≥M2 flares with high values of SXR and ∼1 MHz fluences (&gt;0.1 J m−2 and &gt;6 × 105 sfu × minute, respectively) are both reduced by ∼30%. A somewhat larger percentage decrease of these two parameters (∼40% versus ∼30%) is obtained for the 2006–2014 interval in comparison with 1995–2005. Despite these differences, ESPERTA performance was comparable for the two intervals. For the 2006–2014 interval, ESPERTA had a probability of detection (POD) of 59% (19/32) and a false alarm rate (FAR) of 30% (8/27), versus a POD = 63% (47/75) and an FAR = 42% (34/81) for the original 1995–2005 data set. In addition, for the 2006–2014 interval the median (average) warning time was estimated to be ∼2 hr (∼7 hr), versus ∼6 hr (∼9 hr), for the 1995–2005 data set.}
}
```
```
@article{https://doi.org/10.1029/2007SW000379,
  author = {Laurenza, M. and Cliver, E. W. and Hewitt, J. and Storini, M. and Ling, A. G. and Balch, C. C. and Kaiser, M. L.},
  title = {A technique for short-term warning of solar energetic particle events based on flare location, flare size, and evidence of particle escape},
  journal = {Space Weather},
  volume = {7},
  number = {4},
  pages = {},
  keywords = {solar energetic particles, solar flares, space weather},
  doi = {https://doi.org/10.1029/2007SW000379},
  url = {https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2007SW000379},
  eprint = {https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/2007SW000379},
  abstract = {We have developed a technique to provide short-term warnings of solar energetic proton (SEP) events that meet or exceed the Space Weather Prediction Center threshold of J (>10 MeV) = 10 pr cm−2 s−1 sr−1. The method is based on flare location, flare size, and evidence of particle acceleration/escape as parameterized by flare longitude, time-integrated soft X-ray intensity, and time-integrated intensity of type III radio emission at ∼1 MHz, respectively. In this technique, warnings are issued 10 min after the maximum of ≥M2 soft X-ray flares. For the solar cycle 23 (1995–2005) data on which it was developed, the method has a probability of detection of 63\% (47/75), a false alarm rate of 42\% (34/81), and a median warning time of ∼55 min for the 19 events successfully predicted by our technique for which SEP event onset times were provided by Posner (2007). These measures meet or exceed verification results for competing automated SEP warning techniques but, at the present stage of space weather forecasting, fall well short of those achieved with a human (aided by techniques such as ours) making the ultimate yes/no SEP event prediction. We give some suggestions as to how our method could be improved and provide our flare and SEP event database in the auxiliary material to facilitate quantitative comparisons with techniques developed in the future.},
  year = {2009}
}
```

### MMS Neural Networkds
#### Jonah Ekelund et al. Paper
```
@article{ekelund2024ai,
  title={AI in Space for Scientific Missions: Strategies for Minimizing Neural-Network Model Upload},
  author={Ekelund, Jonah and Vinuesa, Ricardo and Khotyaintsev, Yuri and Henri, Pierre and Delzanno, Gian Luca and Markidis, Stefano},
  journal={arXiv preprint arXiv:2406.14297},
  year={2024}
}
```

#### Vyacheslav Olshevsky Work
##### Olshevsky et al. Paper
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

##### Git Repository
https://bitbucket.org/volshevsky/mmslearning/
