from scapy.all import *
from datetime import datetime
from twilio.rest import Client

account_sid = '...'
auth_token = '...'
client = Client(account_sid, auth_token)

connection_vet = []

class Connection:
    def __init__(self, id, time):
        self.id = id
        self.time = time


def update_or_create(id, time):
    for instance in connection_vet:
        if instance.id == id:
            instance.time = time
            return

    connection_vet.append(Connection(id, time))
    return

def print_pkt(pkt):
    time = datetime.now()
    update_or_create(pkt[Raw].load, time)
    

#ifce = lo, por ser interno.
def sniff_packets():
    pkt = sniff(filter='udp and dst port 12000', prn=print_pkt, iface="lo")


if __name__ == "__main__":
    sniff_thread = threading.Thread(target=sniff_packets)
    sniff_thread.start()

    while True:
        current_time = datetime.now()

        for index, connection in enumerate(connection_vet):
            tempo_decorrido = current_time - connection.time
            tempo_limite = timedelta(seconds=15)
            if tempo_decorrido >= tempo_limite:
                del connection_vet[index]
                with open("log.txt", "a") as my_file:
                    my_file.write(connection.id.decode('utf-8') + ' esta fora do ar!\n')
                    my_file.write('Ultima atualização: ' + current_time.strftime('%H:%M:%S') + '\n')
                    my_file.write('==========================================\n')

                #Outra opção seria utilizar o pywhatkit.
                # pywhatkit.sendwhatmsg_instantly(phone_numer, message, time_hour, time_minute, waiting_time_to_send, close_tab, waiting_time_to_close)
                # message = connection.id.decode('utf-8') + ' esta fora do ar!'
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body= connection.id.decode('utf-8') + ' esta fora do ar!',
                    to='whatsapp:+5516991347493')