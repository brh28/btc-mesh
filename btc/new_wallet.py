import bdkpython as bdk
import json

m = bdk.Mnemonic(bdk.WordCount.WORDS12)

prvKey = bdk.DescriptorSecretKey(
    network=bdk.Network.TESTNET, 
    mnemonic=m,
    password=None
)

pubKey = prvKey.as_public()

jsonOut = { 
    'mnemonic': m.as_string(), 
    'prvKey': prvKey.as_string(),
    'pubKey': pubKey.as_string()
}
print(json.dumps(jsonOut, indent=2))


# TODO
# descStr = f"wsh(pk({extendedKey.as_string()}))"
# desc = bdk.Descriptor(descStr, bdk.Network.TESTNET)
# extendedKey = prvKey.derive(bdk.DerivationPath("m/84'/1'/0'/0"))
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



