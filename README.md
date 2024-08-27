# Flow Log Parser

## Description
This project is a simple Python application that processes flow logs and generates reports based on a lookup table. 
It includes components for parsing lookup tables, processing logs, and writing output.

#### Assumptions made:
1. The Port/Protocol Combination counts will only be counted for the combinations in the flow log file for which the
tags are found in the lookup table
2. Malformed records in the flow file will be categorized under `untagged`
3. The format of the flow file is as follows:
```
80 tcp
443 tcp
999 udp
```
4. CSV file for the lookup table will contain a header, hence the first row is skipped
## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NahushNaik/flow_log_parser.git

2. This project requires `Python 3.9` to be installed   

## Usage
### Running unit tests
1. Navigate to directory `flow_log_parser`
2. Run `python -m unittest discover -s tests`

### Running the program
1. Navigate to directory `flow_log_parser`
2. Run `python -m application.app <path/to/lookup_table.csv> <path/to/flow_log.txt> <path/to/output.txt>`
