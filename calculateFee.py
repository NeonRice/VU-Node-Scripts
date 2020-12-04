from bitcoin.rpc import RawProxy

""" host = "158.129.140.201"
port = "3637"
username = "user030"
password = "g2aFl3e8" """

class Transaction:
    def __init__(self, transactionHash):
        self.hash = transactionHash
        self.info = p.decoderawtransaction(p.getrawtransaction(transactionHash))
        self.vin = self.info['vin']
        self.vout = self.info['vout']
        self.vinValue = self.getInTxValues()
        self.voutValue = self.getOutTxValues()
        self.fee = self.vinValue - self.voutValue
    
    def getInTxValues(self):
        inputValue = 0
        print(self.vin)
        for inputTx in self.vin:
            inputTxID = inputTx['txid']
            inputVoutID = inputTx['vout']
            inputTxInfo = p.decoderawtransaction(p.getrawtransaction(inputTxID))
            inputValue = inputValue + inputTxInfo['vout'][inputVoutID]['value']
        return inputValue

    def getOutTxValues(self):
        outputValue = 0
        for outputTx in self.vout:
            outputValue = outputValue + outputTx['value']
        return outputValue


p = RawProxy()
raw = "2d05f0c9c3e1c226e63b5fac240137687544cf631cd616fd34fd188fc9020866"
transaction = Transaction(raw)
print('Transaction in value: ', transaction.vinValue)
print('Transaction out value: ', transaction.voutValue)
print('Transaction fee ', transaction.fee)