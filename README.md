# Fec-Generator
Python tool that divides transport stream files into data packets and serves them on a multicast network. This tool also generates forward error correction packets from the data packets and serves them on a different port. The correction is column correction as defined in "Pro MPEG Code of Practise#3 release#2"

# How to run
To run program from command line:
* pyton main.py <ts_file_path> <multicast_ip> <port> <duration(sec)> <ts_chunk_size> <D_value> <L_value>
* Ex: python main.py macaskill.ts 224.0.22.2 5555 463 188 8 5
