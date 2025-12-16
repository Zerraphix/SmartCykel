from uthingsboard.client import TBDeviceMqttClient
import network, time, gc, secrets
import alarm

def create_client(alarm_system):
    client = TBDeviceMqttClient(
        secrets.SERVER_IP_ADDRESS,
        access_token=secrets.ACCESS_TOKEN
    )

    def handler(req_id, method, params):
        print("method:", method)
        print("params:", params)
        try:
            if method == "unlockBikeLock":
                solenoid.unlock()
                alarm.request_remote_unlock()
            elif method == "lockBikeLock":
                alarm.Alarm_Lock_System()
            elif method == "testPrint":
                print("RPC testPrint modtaget (ingen lås-bevægelse)")
            else:
                print("Ukendt RPC-metode:", method)
        except TypeError as e:
            print("TypeError in handler:", e)

    client.connect()
    client.set_server_side_rpc_request_handler(handler)

    return client
