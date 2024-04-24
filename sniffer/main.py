from scapy.all import *
from datetime import datetime

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
    #Como ta em LOOP Back o scapy detecta o pacote no momento de emissão e chegada, por isso a duplicata
    time = datetime.now()
    update_or_create(pkt[Raw].load, time)
    

#ifce = lo, por ser interno
def sniff_packets():
    pkt = sniff(filter='udp and dst port 12000', prn=print_pkt, iface="lo")


if __name__ == "__main__":
    sniff_thread = threading.Thread(target=sniff_packets)
    sniff_thread.start()

    while True:
        current_time = datetime.now()

        for index, connection in enumerate(connection_vet):
            tempo_decorrido = current_time - connection.time
            tempo_limite = timedelta(seconds=5)
            if tempo_decorrido >= tempo_limite:
                del connection_vet[index]
                print(f"{connection.id} esta fora do ar")
                
    