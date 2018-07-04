# pyfuzz
## Dependecies
### crc16 : pip3 install crc16
### coverage
## Install
## Usage
## Architecture
  afl <->  fuzzerside app  <->   client  <-> server  <-> translator <-> wrapper <-> python target 
| afl  |    kelinci fuzzerside interface  |   pyfuzz             |   user input  |
## Notes
Parallelizable, also on different machines.
