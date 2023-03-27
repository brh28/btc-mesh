import bdkpython as bdk
import meshtastic.serial_interface
import sys
from segment import Segment
import time

args = sys.argv
raw_tx = args[2]

devPath = str(args[1])
interface = meshtastic.serial_interface.SerialInterface(devPath=devPath)

# gid = self.api_thread.gid.gid_val
gid = 'm1' # Global message identifier: [<nodeId>:<messageIdx>]. Though probably should just be the sender since messageIdx is a seperate param

# (strHexTx, strHexTxHash, network) = rem.split(" ")
strHexTx = str(args[2])
print(f"strHexTx = {strHexTx}")
# trx = bdk.Transaction(strHexTx)
strHexTxHash = "tx_hash"
network='t'

# Would be cooler if type Transaction implemented segment()
segments = Segment.tx_to_segments(
    gid, 
    strHexTx, 
    strHexTxHash, 
    1, # str(self.messageIdx), 
    network, 
    False
)

print(f"Created {len(segments)} chunks.")
for seg in segments :
    print(f"Broadcasting {{{seg}}} to mesh")
    interface.sendData(seg.serialize(), wantAck=True)

# self.messageIdx = (self.messageIdx+1) % 9999












# Send the chunked data over the network, then receive it on the other end
# chunked_data = serialize_and_chunk_data(raw_tx, 40)
# header = chunked_data[0]
# num_chunks = struct.unpack('I', header)[0]
# print(f"Created {num_chunks} chunks.")
# for i in range(0, len(chunked_data)):
#     print(f"Broadcasting chunk {i}")
#     interface.sendData(chunked_data[i], wantAck=True)



############### Reference for constructing transaction ##########
# descriptor = bdk.Descriptor(args[2], bdk.Network.TESTNET) 
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

# wallet = bdk.Wallet(
#              descriptor=descriptor,
#              change_descriptor=None,
#              network=bdk.Network.TESTNET,
#              database_config=db_config,
#          )

# # Create a transaction builder
# txBuilderResult = wallet
#     .build_tx()
#     .set_recipients(vec!((core_address.script_pubkey(), 500000000)))
#     .finish()

# (psbt, _) = txBuilderResult

# # Sign the above psbt with signing option
# wallet.sign(psbt) # returns FfiConverterTypePartiallySignedTransaction

# # Extract the final transaction
# raw_tx = psbt.extract_tx()