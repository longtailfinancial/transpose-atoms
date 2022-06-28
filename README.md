# Transpose Demos

This repo has demo files to demonstrate the functionality of the transpose API suite.

## Contents
### Basics
- Collection Basics
	- Collection Info
	- Collection Image
	- Collection Activity
	- Collection Sales 
- NFT Basics
	- NFT Info
	- NFT Image
	- NFT Activity
	- NFT Sales
- Wallet Basics
	- Wallet Balances
	- Wallet Activity
	- Wallet Sales 

### Low Level Data
- Blocks
- Transactions
- Logs

### Wallet Analysis
- Wallet Balances Analysis
- Wallet Sales Analysis
- Wallet Likeness Analysis
- Wallet NFT Ownership Summary

### Project Analysis
- Project Sales Analysis
- Project Wallet Analytics
- Project Exchange Summary
- Project Wallet Similarity Analysis

### SDK Examples
- Pagination
- Multithreaded Retrieval

## Setup
1. Sign up for a free key at https://transpose.io 
2. `python3 -m venv env`
3. `source env/bin/activate`
4. `python3 -m pip --upgrade pip`
5. `python3 -m pip install -r requirements.txt`
6. `jupyter notebook`

These commands get your environment set up and launch the notebook. You can set up your key as an environment variable or add it **as a string** into the Transpose object initialization.

ex:

`api = Transpose("YOUR_KEY_HERE")`

The rest should work out of the box!