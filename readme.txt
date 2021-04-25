== Description ==

This application retrieves the following statistics through the COVID API Service:
Total Confirmed
Total Death
Total Recovered


== Installation ==
pip install requirements.txt

Change the following in config/covidreport.yml:
excel_driver_path: '/home/developer/code/python/jyputer/config/covidreport.xlsx'
This is the path of date and iso list

iso_country_path: '/home/developer/code/python/jyputer/config/iso_country.xlsx'
This is the path of valid iso list

excel_ouput_path: '/home/developer/code/python/jyputer/covidreport_output.xlsx'
This is the path of statistics
Format: 
date	    iso	confirmed	deaths	recovered
2021-01-01	USA	20128693	347788	0
2021-01-02	CAN	589935	    15707	497492
2021-01-03	CHN	96160	    4784	90159
2021-01-04	BRA	7753752	    196561	6950045


== Execution ==
For the program
python covidreport.py 

For Unit-Test program
python -m unittest test_covidreport.py


