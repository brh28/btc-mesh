import pickle
import struct

def serialize_and_chunk_data(data, chunk_size):
    # Serialize the data
    serialized_data = pickle.dumps(data)

    # Chunk the serialized data into byte streams of a defined size
    chunks = []
    for i in range(0, len(serialized_data), chunk_size):
        chunk = serialized_data[i:i+chunk_size]
        chunks.append(chunk)

    # Pack the chunk information into a binary string
    header = struct.pack('I', len(chunks))

    # Return the header and the chunked data as a list of binary strings
    return [header] + chunks


''' 
This module derived from Rich D's PyMuleTools respository:
https://github.com/kansas-city-bitcoin-developers/PyMuleTools
'''

import json
# from zmq.utils import z85
# import md5
import string

class Segment:

    def __init__(self, _id, payload, tx_hash=None, sequence_num=0, testnet=False, segment_count=None, block=None, message=False):
        self.segment_count = segment_count
        self.tx_hash = tx_hash
        self.payload_id = _id
        self.testnet = testnet
        self.sequence_num = sequence_num
        self.payload = payload
        self.block = block
        self.message = message

    def __str__(self):
        return f"Msg {self.payload_id} Part {self.sequence_num}"

    def __repr__(self):
        return self.serialize_to_json()

    def getPayload(self):
        return f"{self.payload}"

    def serialize(self):
        data = {
            "i": self.payload_id,
            "t": self.payload
        }

        if self.sequence_num > 0:
            data["c"] = self.sequence_num

        if self.sequence_num == 0:
            data["s"] = self.segment_count
            data["h"] = self.tx_hash

        if self.testnet:
            data["n"] = "t"

        if self.message:
            data["n"] = "d"

        # transaction confirmations contain only two elements
        if self.block:
            data = {
                "h": self.tx_hash,
                "b": self.block
            }

        print(f"data = {data}")

        return pickle.dumps(data)
        # return json.dumps(data,separators=(',',':'))

    @classmethod
    def deserialize(cls, bytes_data):
        data = pickle.loads(bytes_data)

        # Validate
        # if not cls.segment_json_is_valid(data):
        #     raise AttributeError(
        #         'Segment JSON is valid but not properly constructed. Refer to MuleTools documentation for details.\r\n\
        #             {json_string}')

        # present for normal segments, but not for block confirmations
        _id = data["i"] if "i" in data else ''
        payload = data["t"] if "t" in data else ''

        # Tail segments
        sequence_num = data["c"] if "c" in data else 0

        # Head segments
        segment_count = data["s"] if "s" in data else None
        tx_hash = data["h"] if "h" in data else None

        # Optional network flag
        testnet = True if "n" in data and data["n"] == "t" else False
        message = True if "n" in data and data["n"] == "d" else False

        # Block confirmation
        block = data["b"] if "b" in data else None

        return cls( _id, payload, tx_hash=tx_hash, sequence_num=sequence_num, testnet=testnet, segment_count=segment_count, block=block,message=message)

    @classmethod
    def segment_json_is_valid(cls, data):
        return ("i" in data and "t" in data and
                (
                        ("s" in data and "h" in data and ("c" not in data or ("c" in data and data["c"] == 0)))
                        or
                        ("c" in data and data["c"] > 0 and "s" not in data and "h" not in data)
                ) or
                ("b" in data and data["b"] >= 0 and "h" in data))

    ## if Z85 encoding, use 24 extra characters for tx in segment0. Hash encoded on 40 characters instead of 64
    ##
    ## This method translated to python from txTenna app PayloadFactory.java : toJSON method
    ##
    ## JSON Parameters
    ##    * **s** - `integer` - Number of segments for the transaction. Only used in the first segment for a given transaction.
    ##    * **h** - `string` - Hash of the transaction. Only used in the first segment for a given transaction. May be Z85-encoded.
    ##    * **n** - `char` (optional) - Network to use. 't' for TestNet3, 'd' for message data, otherwise assume MainNet. Only used in the first segment for a given transaction.
    ##    * **i** - `string` - TxTenna unid identifying the transaction (8 bytes).
    ##    * **c** - `integer` - Sequence number for this segment. May be omitted in first segment for a given transaction (assumed to be 0).
    ##    * **t** - `string` - Hex transaction data for this segment. May be Z85-encoded.
    ##    * **b** - `integer` - Block height of corresponding transaction hash. Will be 0 for mempool transactions.
    @classmethod
    def tx_to_segments(self, device_id, strHexTx, strHexTxHash, messageIdx=0, network='m', isZ85=False):
        # a unique identifier for set of segments from a particular node
        _id = str(device_id) + ":" + str(messageIdx)

        # try :
        #     buf = _id.decode("UTF-8")
        #     md5_hash = md5.new(buf).digest()
        #     idBytes = md5_hash[:8] ## first 8 bytes of md5 digest
        #     if isZ85 :
        #         tx_id = z85.encode(idBytes.encode("hex"))
        #     else :
        #         tx_id = idBytes.encode("hex")
        # except Exception: # pylint: disable=broad-except
        #     return None

        # segment0Len = 100  ## 110?
        # segment1Len = 180  ## 190?
        mtu = 80 # TODO - determine mesh MTU. Can't find in docs. Trial & Error?

        # if isZ85 : 
        #     segment0Len += 24

        strRaw = strHexTx
        # if isZ85 :
        #     strRaw = z85.encode(strHexTx)

        length = len(strRaw)

        seg_count = 0
        if length <= mtu :
            seg_count = 1
        else :
            length -= mtu
            seg_count = 1
            seg_count += (length / mtu)
            if length % mtu > 0 :
                seg_count += 1

        tx_id = messageIdx

        ret = []
        for seg_num in range(0, int(seg_count)) :

            if seg_num == 0 :
                # if isZ85 :
                #     tx_hash = z85.encode(strHexTxHash.decode("hex"))
                # else :
                #     tx_hash = strHexTxHash

                seg_len = len(strRaw)
                print(f"seg_len = {seg_len}")

                tx_seg = strRaw
                if seg_len > mtu :
                    seg_len = mtu
                    tx_seg = strRaw[:seg_len]
                    strRaw = strRaw[seg_len:]
                
                rObj = Segment(_id, tx_seg, tx_hash=strHexTxHash, segment_count=int(seg_count), testnet=(network == 't'), message=(network == 'd'))
                ret.append(rObj)

            else :
                seg_len = len(strRaw)
                tx_seg = strRaw
                if seg_len > mtu :
                    seg_len = mtu
                    tx_seg = strRaw[:seg_len]
                    strRaw = strRaw[seg_len:]

                rObj = Segment(_id, tx_seg, sequence_num=seg_num)
                ret.append(rObj)

        return ret
