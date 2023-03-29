import bdkpython as bdk
import sys
import json

args = sys.argv

m = bdk.Mnemonic(bdk.WordCount.WORDS12)
net = bdk.Network.TESTNET
prvKey = bdk.DescriptorSecretKey(
    network= net, 
    mnemonic=m,
    password=None
)

externalExtendedKey = prvKey.derive(bdk.DerivationPath("m/84'/1'/0'/0"))
desc = bdk.Descriptor(f"wsh(pk({externalExtendedKey.as_string()}))", net)

internalExtendedKey = prvKey.derive(bdk.DerivationPath("m/84'/1'/0'/1"))
internalDesc = bdk.Descriptor(f"wsh(pk({internalExtendedKey.as_string()}))", net)

# bdk.Descriptor("wpkh(tprv8ZgxMBicQKsPcx5nBGsR63Pe8KnRUqmbJNENAfGftF3yuXoMMoVJJcYeUw5eVkm9WBPjWYt6HMWYJNesB5HaNVBaFc1M6dRjWSYnmewUMYy/84h/0h/0h/0/*)", net)

jsonOut = { 
    'mnemonic': m.as_string(), 
    'prvKey': prvKey.as_string(),
    'pubKey': prvKey.as_public().as_string(),
    'descriptor': desc.as_string_private(),
    'change_descriptor': internalDesc.as_string_private()
}
out = json.dumps(jsonOut, indent=2)
print(out)

f = open(args[1] + '.json', "w")
f.write(out)
f.close()


# TODO
# db_config = bdk.DatabaseConfig.MEMORY()
# wallet = bdk.Wallet(
#              descriptor=desc,
#              change_descriptor=None,
#              network=bdk.Network.TESTNET,
#              database_config=db_config,
#          )
# address_info = wallet.get_address(bdk.AddressIndex.LAST_UNUSED())
# address = address_info.address
# print(f"address: {address}")




