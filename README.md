The purpose of this library is to transmit bitcoin objects (addresses, raw_trx, psbt, etc) over a mesh network.

The project uses the bdk-python bindings: https://github.com/bitcoindevkit/bdk-ffi/tree/master/bdk-python

and transmits using the Meshtastic python API: https://python.meshtastic.org/


## Example usage: Sending a new wallet address over the mesh 

This example requires two meshtastic devices. I'm using the [LILYGO T-Beam](https://meshtastic.org/docs/hardware/devices/tbeam/). Use the [Meshtastic documentation](https://meshtastic.org/docs/getting-started) to connect your devices. 

1) From the command line, run the python listener. Make sure to replace the device port argument with whatever port your device is actually on.  
```python3 listen.py /dev/ttyACM0```

2) From a second terminal (on a machine connected to your second mesh device), create a new wallet: 
```
python3 btc/new_wallet.py
{
  "mnemonic": "plastic budget luxury motion suggest effort wisdom unaware arrange emerge soft joke",
  "prvKey": "tprv8ZgxMBicQKsPdTcHupoiwpYiMEUGHPwJEuvvQavhtjKa51teihFZdvwfkwVs2t48hvm171E5qU6pzN1sC9Nrat9s5NBztaNUsoTdtKWMavp/*",
  "pubKey": "tpubD6NzVbkrYhZ4Wve5oUUKMECpvFzCSj8CpDXhh6y1K17xuW9RM659pRZXw7kGgLWwvRvi27hnKgyQNWDbqiyhoxEVRhJ5d8BGHb4GLdgPRpC/*"
}
wsh(pk([e9cf58d4/84'/1'/0'/0]tpubDEkqww1whbUdN8zRuTNQNdSajPbnQQr7K3LfeYeiFBQRFXTX5YkRTasA4SKNkvgUgiKmpjzTy13od5Fosgkp8utsqXnvexJGn15i4qEvsfi/*))#fzhvuejq
```

This outputs a new key-pair plus corresponding descriptor.

3) Copy the descriptor, and run the broadcast_address script:

```
python3 btc/broadcast_address.py /dev/ttyACM1 "wsh(pk([e9cf58d4/84'/1'/0'/0]tpubDEkqww1whbUdN8zRuTNQNdSajPbnQQr7K3LfeYeiFBQRFXTX5YkRTasA4SKNkvgUgiKmpjzTy13od5Fosgkp8utsqXnvexJGn15i4qEvsfi/*))#fzhvuejq"
Broadcasting address tb1qw7a68mqdz3jc9shzpl72s66xps3q6rz2h7hnzyhsh9p88pysmcyqt3u2pk on port /dev/ttyACM1
```

4) From your listener you should see a message with your broadcasted address: 

```
Received: tb1qw7a68mqdz3jc9shzpl72s66xps3q6rz2h7hnzyhsh9p88pysmcyqt3u2pk
```

