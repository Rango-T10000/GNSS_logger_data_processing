# GNSS_logger_data_processing
This is the code to process the data receiving via GNSS_logger. You can get (x,y,z, Satellite_xyz, Carrier_phase, am)
Only use gnss_logger folder is ok.
Because you may have different version of RINEX file, you need to modify the code according to your version.
<img width="1356" alt="image" src="https://github.com/user-attachments/assets/4f3d26cf-1d89-4d17-8a52-f372977c6ce4">
<img width="369" alt="image" src="https://github.com/user-attachments/assets/89bb077c-208b-40d6-9929-04ca0228eba4">

```
conda create -n gps python=3.8 -y
conda activate gps
conda install numpy
conda install pandas
conda install xarray
pip install pymap3d
```
