import binascii
import hashlib

from bitcoin.rpc import RawProxy

class HashValidator:

    def __init__(self, node):
        self.node = node

    def validate(self, blockHeight):
        blockHash = self.node.getblockhash(int(blockHeight))
        blockHeader = self.node.getblockheader(blockHash)

        headerHex = (self.toLittleEndian(blockHeader['versionHex']) +
                     self.toLittleEndian(blockHeader['previousblockhash']) +
                     self.toLittleEndian(blockHeader['merkleroot']) +
                     self.toLittleEndian(format(int(blockHeader['time']), 'x')) +
                     self.toLittleEndian(blockHeader['bits']) +
                     self.toLittleEndian(format(int(blockHeader['nonce']), 'x')))

        headerBinary = binascii.unhexlify(headerHex)
        calculatedHash = self.toLittleEndian(hashlib.sha256(hashlib.sha256(headerBinary).digest()).hexdigest())
        if blockHash == calculatedHash:
            return True
        else:
            return False

    def toLittleEndian(self, input):
        byteArr = bytearray.fromhex(input)
        byteArr.reverse()
        return ''.join(format(x, '02x') for x in byteArr)

node = RawProxy()
block = int(raw_input('Enter a block to validate -> '))
if HashValidator(node).validate(block) :
    print('Block is valid')
else:
    print('Block is invalid')

