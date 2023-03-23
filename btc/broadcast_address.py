import bdkpython as bdk
import meshtastic.serial_interface
import sys

args = sys.argv

descriptor = bdk.Descriptor("wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)", bdk.Network.TESTNET) 
db_config = bdk.DatabaseConfig.MEMORY()
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

wallet = bdk.Wallet(
             descriptor=descriptor,
             change_descriptor=None,
             network=bdk.Network.TESTNET,
             database_config=db_config,
         )

address_info = wallet.get_address(bdk.AddressIndex.LAST_UNUSED())
address = address_info.address

devPath = devPath=str(args[1])
interface = meshtastic.serial_interface.SerialInterface(devPath=devPath)
print(f"Broadcasting address {address} on port {devPath}")
interface.sendText(f"{address}")
