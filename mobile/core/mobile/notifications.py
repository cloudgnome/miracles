# from pyfcm import FCMNotification
from requests import post
from json import dumps

FCM_END_POINT = "https://fcm.googleapis.com/fcm/send"

api_key = 'AAAA4LRVu8w:APA91bGEPbjkE1afa0erF31OlUQ8ng7g1dt98FP2dMJiRhhCiGkAzhsISk8MbqHdwPk3NgMy1YZ1KOa6xtm82sEmlv-J_SBFluPjdOap8svXvFn_n1mgVLvUjn8CKaleTFm6O70AuACv'

headers = {
    "Content-Type": "application/json",
    "Authorization": "key=" + api_key,
}

# push_service = FCMNotification(api_key=api_key)

def send_notification(message_title,message_body,users,order_id):
    for user in users:

        if not user.fcm_token:
            continue

        data = {
            'body':message_body,
            'title':message_title,
            'order_id':order_id
        }
        notification = {
            "title":message_title,
            "body":message_body,
            'sound':'default'
        }
        message = {
            'to':user.fcm_token,
            'data':data,
            "notification":notification,
            'priority':'normal'
        }

        try:
            result = post(FCM_END_POINT, headers=headers, data=dumps(message), timeout=5)
        except:
            pass
