The purpose of this library is to transmit bitcoin objects (addresses, raw_trx, psbt, etc) over a mesh network.

The project uses the bdk-python bindings: https://github.com/bitcoindevkit/bdk-ffi/tree/master/bdk-python

and transmits using the Meshtastic python API: https://python.meshtastic.org/


## Example usage: Sending a transaction address over the mesh 

This example requires two meshtastic devices. I'm using the [LILYGO T-Beam](https://meshtastic.org/docs/hardware/devices/tbeam/). Use the [Meshtastic documentation](https://meshtastic.org/docs/getting-started) to connect your devices. 

1) From your client device, create a new wallet: 
```
python3 btc/new_wallet.py alice             
{
  "mnemonic": "tourist rude cute ring inside opinion unique symbol face physical december charge",
  "prvKey": "tprv8ZgxMBicQKsPd3yjVdadycjPJHhVBLKHDcwWfVK1TEFZFr4dBZQV9eSeFuH4sfJSAqKdPZ9Sg8wLph1chY4NnKbkQ9aZ2gMwGLLDbbVyuxu/*",
  "pubKey": "tpubD6NzVbkrYhZ4WX1XPHFEP2PVsKDRLfWBnvYHx1MJsW3x6LKPoxE5L94WS1CC9tHsax6zf84W9VbbEWCtAzVwQdyUomuTQ6CP3PmMN7BP9mm/*",
  "descriptor": "wsh(pk([24b2e772/84'/1'/0'/0]tprv8hfThZseRyJvPGG8xixBxyRboxB1P3Hi15REsay9pPrswPa3pRh5tKWJj6N5ufShau1VJdJsDvKFfM23Qz4xdy4yPvGFtGNwLftn9FMSMjF/*))#kn8v93p9",
  "change_descriptor": "wsh(pk([24b2e772/84'/1'/0'/1]tprv8hfThZseRyJvRdVHTVQ1EjXbXuYXNpsVS1tAocRZn3t2KnPzmnBpRGrHFQWTS2bs3S9sji4GkbRYqLavCmg5tGCjXpRbKhnRFZ5g2SQav8q/*))#45470s67"
}
```

This outputs a new key-pair plus corresponding private descriptors.

2) Get an address from the new wallet:

```
python3 btc/get_address.py alice  
tb1qewwd4z3w7phsjucqkek9jgs5dqwsky3rhdrk58vvlce08zeqnyjqaue8lq
```
3) Sends testnet BTC to the address from step 3 using the [faucet](https://bitcoinfaucet.uo1.net/send.php).

4) Once the receive transaction has completed, start the listener from the machine you wish to act as your bridge between the internet and the mesh:

```
python3 btc/listen.py /dev/ttyACM0
```
*Make sure to replace the device port argument with whatever port your device is actually on. 

5) From a second terminal (on a machine connected to your second mesh device), broadcast your trx:

```
python3 btc/broadcast_tx.py carol /dev/ttyACM1
```

*If all went smoothly, you should see in output in your listener similar to this:

```
Msg m1:1 Part 0
Msg m1:1 Part 2
Msg m1:1 Part 3
Msg m1:1 Part 4
Msg m1:1 Part 5
Msg m1:1 Part 1
Broadcasting trx: 010000000001028be6de33e33b9d32ce80653d2375584ed4bfdcc8645df6eef0867145f5b47a120100000000feffffff8be6de33e33b9d32ce80653d2375584ed4bfdcc8645df6eef0867145f5b47a120000000000feffffff02e80300000000000022002039666090ffa3ba190b5cfc9114091c8462e224ac8b8943d02847a875b66af1515702000000000000220020005a59daacdccbc5b145b9ce5401e7caf07d274e6905b0e7dfa8e5689dfd31ce02473044022050cae193f8b17754701ae94376f630dfa82765772a7515209defc80c9d090fc5022040b8c013561dfab491464e6fbc3866f727c2e08ebf7ece8606f743ba236c2559012321037cc42af63d8aa5b9f0552c021624155d5bac27c9ce50b4e17acbf5c576b94d1fac0247304402201090c93ab3994e87dcbb8386825c8383356abf5c3742a49717afc785d0e6155402204be16ded1132cc5064fae6166ddc6c175f3e46d5c33c95d72d47e5c1d89129e601232103e5cb462e283b9053c8667b6b8546495a43ae6d4161b527475fe2612ce4ca6eadac41062500
Successfully broadcasted: 45131bc11527cd250c7b4494024706a872532922f504e9222c99fbfe3d851343
```


