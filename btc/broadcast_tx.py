import bdkpython as bdk
import meshtastic.serial_interface
import sys
from segment import Segment
import json
import time

def wallet_from_file(fileName):
    f = open(args[1] + '.json', "r")
    walletJson = json.loads(f.read())
    db_config = bdk.DatabaseConfig.MEMORY()
    return bdk.Wallet(
        descriptor=bdk.Descriptor(walletJson['descriptor'], bdk.Network.TESTNET),
        change_descriptor=bdk.Descriptor(walletJson['change_descriptor'], bdk.Network.TESTNET),
        network=bdk.Network.TESTNET,
        database_config=db_config,
    )

args = sys.argv

wallet = wallet_from_file(args[1] + '.json')
blockchain_config = bdk.BlockchainConfig.ELECTRUM(
    bdk.ElectrumConfig(
        "ssl://electrum.blockstream.info:60002",
        None,
        5,
        None,
        100,
        True,
    )
)
blockchain = bdk.Blockchain(blockchain_config)
wallet.sync(blockchain, None) # TODO - how to sync without Blockchain config

print(f"balance = {wallet.get_balance()}")

faucet_address = bdk.Address("tb1q89nxpy8l5wapjz6uljg3gzgus33wyf9v3wy585pgg758tdn279gs05t3ev")
tx = bdk.TxBuilder().add_recipient(faucet_address.script_pubkey(), 1000).finish(wallet)

print(f"transaction_details = {tx.transaction_details}")

psbt = tx.psbt
signed_psbt = wallet.sign(psbt)

print(f"signed_psbt = {signed_psbt}")

raw_transaction = psbt.extract_tx()

gid = 'm1' 

strHexTx = ''.join(map(lambda x: format(x, '02x'), raw_transaction.serialize()))
print(f"strHexTx = {strHexTx}")

# trx = bdk.Transaction(strHexTx)
strHexTxHash = "tx_hash"
network='t'

# Would be cooler if type Transaction implemented segment()
segments = Segment.tx_to_segments(
    gid, 
    raw_transaction.serialize(), 
    tx.transaction_details.txid, 
    1, # str(self.messageIdx), 
    network, 
    False
)


devPath = str(args[2])
interface = meshtastic.serial_interface.SerialInterface(devPath=devPath)

print(f"Broadcasting {strHexTxHash} over mesh in {len(segments)} parts")
for seg in segments :
    print(f"Broadcasting {{{seg}}} to mesh")
    interface.sendData(seg.serialize(), wantAck=True)
