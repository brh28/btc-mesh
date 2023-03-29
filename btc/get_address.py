import bdkpython as bdk
import meshtastic.serial_interface
import sys
import json

args = sys.argv

# db_config = bdk.DatabaseConfig.MEMORY()
# blockchain_config = bdk.BlockchainConfig.ELECTRUM(
#     bdk.ElectrumConfig(
#         "ssl://electrum.blockstream.info:60002",
#         None,
#         5,
#         None,
#         100,
#         True,
#     )
# )
# blockchain = bdk.Blockchain(blockchain_config)
# sync

f = open(args[1] + '.json', "r")
walletJson = json.loads(f.read())
db_config = bdk.DatabaseConfig.MEMORY()
wallet = bdk.Wallet(
             descriptor=bdk.Descriptor(walletJson['descriptor'], bdk.Network.TESTNET),
             change_descriptor=bdk.Descriptor(walletJson['change_descriptor'], bdk.Network.TESTNET),
             network=bdk.Network.TESTNET,
             database_config=db_config,
         )

address_info = wallet.get_address(bdk.AddressIndex.LAST_UNUSED())
address = address_info.address
print(f"{address}")


#########FOR BROADCASTING##################
# devPath = devPath=str(args[1])
# interface = meshtastic.serial_interface.SerialInterface(devPath=devPath)
# print(f"Broadcasting address {address} on port {devPath}")
# interface.sendText(f"{address}")
