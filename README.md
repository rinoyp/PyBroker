# PyBroker

An open source library for testing trading algorithms with real data. Currently in development.

## Dependencies
- pandas

## How to Use
1. Download data from http://stocks.rinoyp.com/data.zip and unzip in root directory
3. Open __main__.py and set the trader capital and length of time to trade for
2. Run with:
```python PyBroker```

## Writing custom strategies
Subclass the Strategy class and override the trade_for_day function. Making sure to call super when done trading for the day.
Currently can only buy stocks. Shorting stocks and options trading not yet supported. 
