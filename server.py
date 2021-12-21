import json
import socket
import threading

import pika
from employee import Employee


class ClientThread(threading.Thread):

    def __init__(self, client_address, client_socket, identity):
        threading.Thread.__init__(self)
        self.c_socket = client_socket
        print("Connection no. " + str(identity))
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", clientAddress)
        e1 = Employee("John")
        e2 = Employee("Paul")
        e3 = Employee("Neel")
        e4 = Employee("Dev")

        e1.setBonus(2018)
        e1.setBonus(2019)
        e1.setHolidayTaken(2018)
        e1.setHolidayTaken(2019)
        e1.setSalaryforYear(2018)
        e1.setSalaryforYear(2019)

        e2.setBonus(2018)
        e2.setBonus(2019)
        e2.setHolidayTaken(2018)
        e2.setHolidayTaken(2019)
        e2.setSalaryforYear(2018)
        e2.setSalaryforYear(2019)

        e3.setBonus(2018)
        e3.setBonus(2019)
        e3.setHolidayTaken(2018)
        e3.setHolidayTaken(2019)
        e3.setSalaryforYear(2018)
        e3.setSalaryforYear(2019)

        e4.setBonus(2018)
        e4.setBonus(2019)
        e4.setHolidayTaken(2018)
        e4.setHolidayTaken(2019)
        e4.setSalaryforYear(2018)
        e4.setSalaryforYear(2019)

        employees = [e1, e2, e3, e4]

        Format = "utf-8"

        commands = []
        name = ""

        while True:
            data = self.c_socket.recv(1024)
            empID = int(data.decode())
            # id is the index of employees
            if empID < len(employees):
                commands.append(empID)
                name = employees[empID].getName()
                print(name)
                self.c_socket.send(bytes(name, Format))  # send salary or leave
                sOrl = self.c_socket.recv(1024)
                msg2 = sOrl.decode()
                commands.append(msg2)
                if msg2 == 'SC':
                    sal = str(employees[empID].getSalary())
                    self.c_socket.send(bytes("Current basic salary ", Format) + bytes(sal, Format))

                elif msg2 == 'ST':
                    self.c_socket.send(bytes("What year?", Format))
                    yr = self.c_socket.recv(1024)
                    year = int(yr.decode())
                    bonus = str(employees[empID].getBonus(year))
                    sal = str(employees[empID].getSalaryByYear(year))
                    self.c_socket.send(
                        bytes("Total salary :", Format) + bytes("basic pay, ", Format) + bytes(sal, Format) + bytes(
                            " Overtime:", Format) + bytes(bonus, Format))

                elif msg2 == 'LC':
                    holiday = str(employees[empID].HolidayEntitlement())
                    self.c_socket.send(bytes("Current annual leave entitlement ", Format) + bytes(holiday, Format))

                # msg == 'LY'
                else:
                    self.c_socket.send(bytes("What year?", Format))
                    yr = self.c_socket.recv(1024)
                    year = int(yr.decode())
                    leave = str(employees[empID].getHolidayTaken(year))
                    self.c_socket.send(bytes("Leave taken :", Format) + bytes(leave, Format))
            else:
                self.c_socket.send(bytes("NAN", Format))
            cont = self.c_socket.recv(1024)
            if cont.decode() == "C":
                continue
            else:
                break
        print("Client at ", clientAddress, " disconnected...")

        message = [name, clientAddress, commands]
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='my-queue')
        channel.basic_publish(exchange='',
                              routing_key='my-queue',
                              body=bytes(json.dumps(message), Format))


LOCALHOST = "127.0.0.1"
PORT = 64001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Server started")
print("Waiting for client request..")

counter = 0

while True:
    server.listen(1)
    my_socket, clientAddress = server.accept()
    counter = counter + 1
    new_thread = ClientThread(clientAddress, my_socket, counter)
    new_thread.start()
