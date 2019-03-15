from Crypto.PublicKey import RSA
from mixin_api import MIXIN_API
import uuid
import mixin_config
import json
import csv
import time
import uuid
import umsgpack
import base64

PIN             = "945689";
PIN2            = "845689";
MASTER_ID       = "37222956";
EXINCORE_UUID   = "61103d28-3ac2-44a2-ae34-bd956070dab1"
MASTER_UUID     = "28ee416a-0eaa-4133-bc79-9676909b7b4e";
BTC_ASSET_ID    = "c6d0c728-2624-429b-8e0d-d9d19b6592fa";
EOS_ASSET_ID    = "6cfe566e-4aad-470b-8c9a-2fd35b49c68d";
USDT_ASSET_ID   = "815b0b1a-2764-3736-8faa-42d694fa620a"
BTC_WALLET_ADDR = "14T129GTbXXPGXXvZzVaNLRFPeHXD1C25C";
AMOUNT          = "0.001";

# // Mixin Network support cryptocurrencies (2019-02-19)
# // |EOS|6cfe566e-4aad-470b-8c9a-2fd35b49c68d
# // |CNB|965e5c6e-434c-3fa9-b780-c50f43cd955c
# // |BTC|c6d0c728-2624-429b-8e0d-d9d19b6592fa
# // |ETC|2204c1ee-0ea2-4add-bb9a-b3719cfff93a
# // |XRP|23dfb5a5-5d7b-48b6-905f-3970e3176e27
# // |XEM|27921032-f73e-434e-955f-43d55672ee31
# // |ETH|43d61dcd-e413-450d-80b8-101d5e903357
# // |DASH|6472e7e3-75fd-48b6-b1dc-28d294ee1476
# // |DOGE|6770a1e5-6086-44d5-b60f-545f9d9e8ffd
# // |LTC|76c802a2-7c88-447f-a93e-c29c9e5dd9c8
# // |SC|990c4c29-57e9-48f6-9819-7d986ea44985
# // |ZEN|a2c5d22b-62a2-4c13-b3f0-013290dbac60
# // |ZEC|c996abc9-d94e-4494-b1cf-2a3fd3ac5714
# // |BCH|fd11b6e3-0b87-41f1-a41f-f0e9b49e5bf0

def pubkeyContent(inputContent):
    contentWithoutHeader= inputContent[len("-----BEGIN PUBLIC KEY-----") + 1:]
    contentWithoutTail = contentWithoutHeader[:-1 * (len("-----END PUBLIC KEY-----") + 1)]
    contentWithoutReturn = contentWithoutTail[:64] + contentWithoutTail[65:129] + contentWithoutTail[130:194] + contentWithoutTail[195:]
    return contentWithoutReturn

def generateMixinAPI(private_key,pin_token,session_id,user_id,pin,client_secret):
    mixin_config.private_key       = private_key
    mixin_config.pin_token         = pin_token
    mixin_config.pay_session_id    = session_id
    mixin_config.client_id         = user_id
    mixin_config.client_secret     = client_secret
    mixin_config.pay_pin           = pin
    return  MIXIN_API(mixin_config)

def readAssetBalance(asset_id):
    with open('new_users.csv', newline='') as csvfile:
        reader  = csv.reader(csvfile)
        for row in reader:
            pin         = row.pop()
            userid      = row.pop()
            session_id  = row.pop()
            pin_token   = row.pop()
            private_key = row.pop()
            mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                        pin_token,
                                                        session_id,
                                                        userid,
                                                        pin,"")
            btcInfo = mixinApiNewUserInstance.getAsset(asset_id)
            print("Account %s \'s balance is %s  " %(userid,btcInfo.get("data").get("balance")))

def readAssetAddress(asset_id,isBTC = True):
    with open('new_users.csv', newline='') as csvfile:
        reader  = csv.reader(csvfile)
        for row in reader:
            pin         = row.pop()
            userid      = row.pop()
            session_id  = row.pop()
            pin_token   = row.pop()
            private_key = row.pop()
            mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                        pin_token,
                                                        session_id,
                                                        userid,
                                                        pin,"")
            btcInfo = mixinApiNewUserInstance.getAsset(asset_id)
            print(btcInfo)
            if isBTC:
                print("Account %s \'s Bitcoin wallet address is %s  " %(userid,btcInfo.get("data").get("public_key")))
            else:
                print("Account %s \'s EOS account name is %s, wallet address is %s  " %(userid,
                                                                        btcInfo.get("data").get("account_name"),
                                                                        btcInfo.get("data").get("account_tag")))

            # print(btcInfo.get("data").get("public_key"))
def gen_memo_ExinBuy(asset_id_string):
    return base64.b64encode(umsgpack.packb({"A": uuid.UUID("{" + asset_id_string + "}").bytes})).decode("utf-8")


mixinApiBotInstance = MIXIN_API(mixin_config)

PromptMsg = "0: Read first user from local file new_users.csv\n"
PromptMsg += "1: \n2: Read account asset balance \n3: Read Bitcoin \n4: Read USDT\n"
PromptMsg += "5: Read transaction of my account\n6: Pay USDT to ExinCore to buy BTC\n7: Create wallet and update PIN\n"
PromptMsg += "8: transafer all asset to my account in Mixin Messenger \n9: Withdraw BTC to another Bitcoin wallet\na: Verify Pin\nd: Create Address and Delete it\nr: Create Address and read it\n"
PromptMsg += "q: Exit \nMake your choose:"
while ( 1 > 0 ):
    cmd = input(PromptMsg)
    if (cmd == 'q' ):
        exit()
    print("Run...")
    if ( cmd == '0'):
        with open('new_users.csv', newline='') as csvfile:
            reader  = csv.reader(csvfile)
            row = next(reader)
            pin         = row.pop()
            userid      = row.pop()
            session_id  = row.pop()
            pin_token   = row.pop()
            private_key = row.pop()
            mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
            print("read user id:" + userid)
    if ( cmd == '2' ):
        AssetsInfo = mixinApiNewUserInstance.getMyAssets()
        print("Your asset balance is\n===========")
        for eachAssest in AssetsInfo:
            print("%s: %s" %(eachAssest.get("name"), eachAssest.get("balance")))
        print("===========")


        availableAssset = []
        for eachAssetInfo in AssetsInfo: 
            if (eachAssetInfo.get("balance") == "0"):
                continue
            if (float(eachAssetInfo.get("balance")) > 0):
                availableAssset.append(eachAssetInfo)
    if ( cmd == '3' ):
        asset_result = mixinApiNewUserInstance.getAsset(BTC_ASSET_ID)
        btcInfo = asset_result.get("data")
        print("%s: %s, depositAddress: %s" %(btcInfo.get("name"), btcInfo.get("balance"), btcInfo.get("public_key")))

    if ( cmd == '4' ):
        asset_result = mixinApiNewUserInstance.getAsset(USDT_ASSET_ID)
        usdtInfo = asset_result.get("data")
        print("%s: %s, depositAddress: %s" %(usdtInfo.get("name"), usdtInfo.get("balance"), usdtInfo.get("public_key")))

    if ( cmd == '6' ):
        # Pack memo
        memo_for_exin = gen_memo_ExinBuy(BTC_ASSET_ID)

        btcInfo = mixinApiNewUserInstance.getAsset(USDT_ASSET_ID)
        remainUSDT = btcInfo.get("data").get("balance")
        print("You have : " + remainUSDT + " USDT")
        this_uuid = str(uuid.uuid1())
        print("uuid is: " + this_uuid)
        confirm_payUSDT = input("Input Yes to pay " + remainUSDT + " to ExinCore to buy Bitcoin")
        if ( confirm_payUSDT == "Yes" ):
            transfer_result = mixinApiNewUserInstance.transferTo(EXINCORE_UUID, USDT_ASSET_ID, remainUSDT, memo_for_exin, this_uuid)
            snapShotID = transfer_result.get("data").get("snapshot_id")
            print("Pay USDT to ExinCore to buy BTC by uuid:" + this_uuid + ", you can verify the result on https://mixin.one/snapshots/" + snapShotID)
    if ( cmd == '7' ):
        key = RSA.generate(1024)
        pubkey = key.publickey()
        print(key.exportKey())
        print(pubkey.exportKey())
        private_key = key.exportKey()
        session_key = pubkeyContent(pubkey.exportKey())
        # print(session_key)
        print(session_key.decode())
        userInfo = mixinApiBotInstance.createUser(session_key.decode(),"Tom Bot")
        print(userInfo.get("data").get("user_id"))
        with open('new_users.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([private_key.decode(),
                                userInfo.get("data").get("pin_token"),
                                userInfo.get("data").get("session_id"),
                                userInfo.get("data").get("user_id"),
                                PIN])
        mixinApiNewUserInstance = generateMixinAPI(private_key.decode(),
                                                    userInfo.get("data").get("pin_token"),
                                                    userInfo.get("data").get("session_id"),
                                                    userInfo.get("data").get("user_id"),
                                                    PIN,"")
        pinInfo = mixinApiNewUserInstance.updatePin(PIN,"")
        print(pinInfo)
        time.sleep(3)
        # mixinApiNewUserInstance.pay_pin = PIN
        pinInfo2 = mixinApiNewUserInstance.verifyPin()
        print(pinInfo2)

    if ( cmd == '5' ):
        timestamp = input("input timestamp, history after the time will be searched:")
        limit = input("input max record you want to search:")
        snapshots_result_of_account = mixinApiNewUserInstance.account_snapshots_after(timestamp, asset_id = "", limit=limit)
        USDT_Snapshots_result_of_account = mixinApiNewUserInstance.find_mysnapshot_in(snapshots_result_of_account)
        for singleSnapShot in USDT_Snapshots_result_of_account:
            amount_snap = singleSnapShot.get("amount")
            asset_snap = singleSnapShot.get("asset").get("name")
            created_at_snap = singleSnapShot.get("created_at")
            memo_at_snap = singleSnapShot.get("data")
            id_snapshot = singleSnapShot.get("snapshot_id")
            opponent_id_snapshot = singleSnapShot.get("opponent_id")
            if((float(amount_snap)) < 0):
                try:
                    exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
                    asset_uuid_in_myorder = str(uuid.UUID(bytes = exin_order["A"]))
                    if(asset_uuid_in_myorder == BTC_ASSET_ID):
                        print(created_at_snap + ": You pay " + amount_snap + " " + asset_snap + " to buy BTC from ExinCore")
                except :
                    print(created_at_snap + ": You pay " + str(amount_snap) + " " + asset_snap + " to " + opponent_id_snapshot +  " with memo:" + memo_at_snap)

            if((float(amount_snap)) > 0 and memo_at_snap):
                try:
                    exin_order = umsgpack.unpackb(base64.b64decode(memo_at_snap))
                    if ("C" in exin_order):
                        order_result = exin_order["C"]
                        headString = created_at_snap +": status of your payment to exin is : "
                        if(order_result == 1000):
                            headString = headString + "Successful Exchange"
                        if(order_result == 1001):
                            headString = headString + "The order not found or invalid"
                        if(order_result == 1002):
                            headString = headString + "The request data is invalid"
                        if(order_result == 1003):
                            headString = headString + "The market not supported"
                        if(order_result == 1004):
                            headString = headString + "Failed exchange"
                        if(order_result == 1005):
                            headString = headString + "Partial exchange"
                        if(order_result == 1006):
                            headString = headString + "Insufficient pool"
                        if(order_result == 1007):
                            headString = headString + "Below the minimum exchange amount"
                        if(order_result == 1008):
                            headString = headString + "Exceeding the maximum exchange amount"
                        if ("P" in exin_order):
                            headString = headString + ", your order is executed at price:" +  exin_order["P"] + " USDT" +  " per " + asset_snap
                        if ("F" in exin_order):
                            headString = headString + ", Exin core fee is " + exin_order["F"] + " with fee asset" + str(uuid.UUID(bytes = exin_order["FA"]))
                        if ("T" in exin_order):
                            if (exin_order["T"] == "F"):
                                headString = headString +", your order is refund to you because your memo is not correct"
                            if (exin_order["T"] == "R"):
                                headString = headString +", your order is executed successfully"
                            if (exin_order["T"] == "E"):
                                headString = headString +", exin failed to execute your order"
                        if ("O" in exin_order):
                            headString = headString +", trace id of your payment to exincore is " + str(uuid.UUID(bytes = exin_order["O"]))
                        print(headString)
                except :
                    print(created_at_snap +": You receive: " + str(amount_snap) + " " + asset_snap + " from " + opponent_id_snapshot + " with memo:" + memo_at_snap)
# c6d0c728-2624-429b-8e0d-d9d19b6592fa
    if ( cmd == '8' ):
        AssetsInfo = mixinApiNewUserInstance.getMyAssets()
        availableAssset = []
        for eachAssetInfo in AssetsInfo: 
            if (eachAssetInfo.get("balance") == "0"):
                continue
            if (float(eachAssetInfo.get("balance")) > 0):
                availableAssset.append(eachAssetInfo)
                print("You have : " + eachAssetInfo.get("balance") + eachAssetInfo.get("name"))
                this_uuid = str(uuid.uuid1())
                print("uuid is: " + this_uuid)
                confirm_pay= input("type YES to pay " + eachAssetInfo.get("balance")+ " to MASTER ")
                if ( confirm_pay== "YES" ):
                    transfer_result = mixinApiNewUserInstance.transferTo(MASTER_UUID, eachAssetInfo.get("asset_id"), eachAssetInfo.get("balance"), "", this_uuid)
                    snapShotID = transfer_result.get("data").get("snapshot_id")
                    print("Pay BTC to Master ID with trace id:" + this_uuid + ", you can verify the result on https://mixin.one/snapshots/" + snapShotID)
    if ( cmd == '9' ):
        with open('new_users.csv', newline='') as csvfile:
            reader  = csv.reader(csvfile)
            for row in reader:
                pin         = row.pop()
                userid      = row.pop()
                session_id  = row.pop()
                pin_token   = row.pop()
                private_key = row.pop()
                print(pin)
                mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
                eosInfo = mixinApiBotInstance.createAddressEOS(EOS_ASSET_ID,"eoswithmixin","d80363afcc466fbaf2daa7328ae2adfa")
                # mixinApiBotInstance.withdrawals(btcInfo.get("data").get("address_id"),AMOUNT,"")
                print(eosInfo)
    if ( cmd == 'a' ):
        with open('new_users.csv', newline='') as csvfile:
            reader  = csv.reader(csvfile)
            for row in reader:
                pin         = row.pop()
                userid      = row.pop()
                session_id  = row.pop()
                pin_token   = row.pop()
                private_key = row.pop()
                print(pin)
                mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
                btcInfo = mixinApiNewUserInstance.verifyPin()
                print(btcInfo)
    if ( cmd == 'd' ):
        with open('new_users.csv', newline='') as csvfile:
            reader  = csv.reader(csvfile)
            for row in reader:
                pin         = row.pop()
                userid      = row.pop()
                session_id  = row.pop()
                pin_token   = row.pop()
                private_key = row.pop()
                print(pin)
                mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
                btcInfo = mixinApiBotInstance.createAddress(BTC_ASSET_ID, BTC_WALLET_ADDR,"BTC","","")
                addr_id = btcInfo.get("data").get("address_id")
                print(addr_id)
                delInfo = mixinApiBotInstance.delAddress(addr_id)
                print(delInfo)
    if ( cmd == 'r' ):
        with open('new_users.csv', newline='') as csvfile:
            reader  = csv.reader(csvfile)
            for row in reader:
                pin         = row.pop()
                userid      = row.pop()
                session_id  = row.pop()
                pin_token   = row.pop()
                private_key = row.pop()
                print(pin)
                mixinApiNewUserInstance = generateMixinAPI(private_key,
                                                            pin_token,
                                                            session_id,
                                                            userid,
                                                            pin,"")
                btcInfo = mixinApiBotInstance.createAddress(BTC_ASSET_ID, BTC_WALLET_ADDR,"BTC","","")
                addr_id = btcInfo.get("data").get("address_id")
                print(addr_id)
                addrInfo = mixinApiBotInstance.getAddress(addr_id)
                print(addrInfo)
