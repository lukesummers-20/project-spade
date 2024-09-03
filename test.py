import os
import json
import time
from hedera import (
    AccountId, 
    PrivateKey,
    Client,
    Hbar,
    PrivateKey,
    AccountCreateTransaction,
    AccountDeleteTransaction,
    TransferTransaction,
    TokenCreateTransaction,
    TokenAssociateTransaction,
    TokenGrantKycTransaction,
    TokenWipeTransaction,
    TokenDeleteTransaction,
    TokenType,
    TokenMintTransaction,
    TokenId,
    )
from jnius import autoclass

OPERATOR_ID = AccountId.fromString("0.0.4806930")
OPERATOR_KEY = PrivateKey.fromString("fe02b50e728558ed78adc0321e1a45c019c8153e056e843e336e2dab7b9fb648")

client = Client.forTestnet()
client.setOperator(OPERATOR_ID, OPERATOR_KEY)

Collections = autoclass("java.util.Collections")
nodeIds = Collections.singletonList(client.network.nodes.toArray()[0].accountId)
txn = (TokenCreateTransaction()
       .setNodeAccountIds(nodeIds)
       .setTokenName("Spade")
       .setTokenSymbol("SPD")
       .setTokenType(TokenType.valueOf('NON_FUNGIBLE_UNIQUE'))
       .setTreasuryAccountId(OPERATOR_ID)
       .setAdminKey(OPERATOR_KEY.getPublicKey())
       .setFreezeKey(OPERATOR_KEY.getPublicKey())
       .setWipeKey(OPERATOR_KEY.getPublicKey())
       .setKycKey(OPERATOR_KEY.getPublicKey())
       .setSupplyKey(OPERATOR_KEY.getPublicKey())
       .setFreezeDefault(False)
       .execute(client))
tokenId = txn.getReceipt(client).tokenId

cid = "ipfs://QmbXzHvjngft1UH5Q6JDnmwqHChayr2cNBE8jgZpR7Pbvk/nft.json"
txn = (TokenMintTransaction()
       .setTokenId(tokenId)
       .addMetadatA(cid.encode())
       .execute(client))
receipt = txn.getReceipt(client)