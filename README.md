# Moviesax's Readme

This simple project demonstrate using FileCoin and IPFS network to save and play video.

Backend: 
- Using Powergate to push data to cold and hot storage
- PyGate to connect from Python script
- PostGresSQL to store database that mapping CID and movie 
- PostGresSQL stores movie meta data (plot, review etc)
- IPFS Python client to download file

Front-end:
- Python Django as frontend
- Video.js to play video


Video is stored in hot and cold storage. Once user choose to view video,
it will check if the video is cached, then play immediately.
Otherwise, it download the video to  the cache location.


