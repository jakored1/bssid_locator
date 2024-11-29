# Apple BSSID Locator  
This script locates BSSIDs via Apples geo-location services  
## Setup & Usage:  
#### Without Docker  
```bash
# Install requirements
sudo apt install -y python3-full python3-protobuf python3-pycurl

# Clone repo
git clone https://github.com/jakored1/bssid_locator.git
cd bssid_locator

# Run script
python3 ./main.py <BSSID>
# python3 ./main.py AA:BB:CC:DD:EE:FF
```
#### With Docker  
```bash
# Clone repo
git clone https://github.com/jakored1/bssid_locator.git
cd bssid_locator

# Build image
docker build -t bssid_locator --no-cache .
# Run and pass BSSID as final argument
docker run --rm bssid_locator <BSSID>
# docker run --rm bssid_locator AA:BB:CC:DD:EE:FF
```
