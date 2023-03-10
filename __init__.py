#!/usr/bin/python3

"""
postcodeDecoder

author: mm

Dekodiere Postcode/Zielcode der 'Deutschen Post'

Eingegeben werden die Nummern 1 und 0.
Dabei entspricht die Nummer 1 einem Strich und die Nummer 0 keinem Strich.

Zielcodes sind genau 80 bits lang und beginnen immer mit '| |' und enden mit '|||'.
"""

class Postcode:

    def __init__(self, code):
        code = code.strip().strip('0')
        if not (code.startswith('101') and code.endswith('111')):
            code = "".join(reversed(code))
            if not (code.startswith('101') and code.endswith('111')):
                print('\n'+'\t\033[95mEs kann kein Anfang gefunden werden!\033[0m')
                raise ValueError()
        if len(code) != 80:
            print('\n'+'\t\033[95mDie Länge der eingegebenen Zeichenkette ist nicht 80 Zeichen!\033[0m')
            raise ValueError()
        for i in code:
            if i not in ('1','0'):
                print('\n'+'\t\033[95mDie Zeichenkette beinhaltet falsche Zeichen!\033[0m')
                raise ValueError()
        self.code = code.translate(str.maketrans('10', '| '))
        self.entgelts = code[2:6], code[7:11]
        self.hausnummer = code[12:16], code[17:21], code[22:26]
        self.strasse = code[27:31], code[32:36], code[37:41]
        self.postleitzahl = code[42:47], code[48:53], code[54:59], code[60:65], code[66:71] 
        self.pruefziffer = code[72:77]
        return None

    @classmethod
    def decode4bs(cls, code) -> int:
        if code.count('0') > 2:
            print("\n'+'\t\033[95mProblem in der 4-bit dekodierung!\033[0m")
            raise ValueError()
        result = 0
        if code[0] == '0': result += 8
        if code[1] == '0': result += 4
        if code[2] == '0': result += 2
        if code[3] == '0': result += 1
        if result == 10: result = 7
        return result

    @classmethod
    def decode5bs(cls, code) -> int:
        if code.count('0') != 2:
            print("\n'+'\t\033[95mProblem in der 5-bit dekodierung!\033[0m")
            raise ValueError()
        result = 0
        if code[0] == '0': result += 0
        if code[1] == '0': result += 1
        if code[2] == '0': result += 2
        if code[3] == '0': result += 4
        if code[4] == '0': result += 7
        return result
    
    @property
    def decoded(self) -> tuple:
        d4bs2int = lambda x: int(''.join(str(self.decode4bs(i)) for i in x)[::-1])
        d5bs2int = lambda x: int(''.join(str(self.decode5bs(i)) for i in x)[::-1])
        entgelts = d4bs2int(self.entgelts)
        hausnummer = d4bs2int(self.hausnummer)
        strassennummer = d4bs2int(self.strasse)
        plz = d5bs2int(self.postleitzahl)
        quersumme = sum(self.decode5bs(i) for i in self.postleitzahl)
        pruefziffer = self.decode5bs(self.pruefziffer)
        sumcheck = 'OK!' if sum((quersumme,pruefziffer)) % 10 == 0 else 'NICHT OK!'
        redOrGreen = '\033[92m' if sum((quersumme,pruefziffer)) % 10 == 0 else '\033[91m'
        output = f"""  \033[90m{self.code}\033[0m Zielcode\n
    ┌{'─'*28}┐
    │ {'Entgelts.:'.ljust(26-len(str(entgelts)), '-')}{entgelts} │
    │ {'Hausnummer:'.ljust(26-len(str(hausnummer)), '-')}{hausnummer} │
    │ {'Straße:'.ljust(26-len(str(strassennummer)), '-')}{strassennummer} │
    │ {'Postleitzahl:'.ljust(26-len(str(plz)), '-')}{plz} │
    │ {'Prüfziffer:'.ljust(26-len(str(pruefziffer)), '-')}{pruefziffer} │
    └{'─'*28}┘
    {redOrGreen}┌{'─'*28}┐
    │\033[0m {'PLZ Quersumme:'.ljust(17)}{quersumme:9}{redOrGreen} │
    │\033[0m {'PLZ Prüfung:'.ljust(17)}{redOrGreen}{sumcheck.rjust(9)} │
    └{'─'*28}┘\033[0m\n"""
        print(output)
        return entgelts, hausnummer, strassennummer, plz, pruefziffer

if __name__ == "__main__":

    write_to_file = False
    error_while_processing = False
    prompt = """
    Eingegeben werden die Nummern 1 und 0.\n    Dabei entspricht die Nummer 1 einem Strich und die Nummer 0 keinem Strich.\n
    Zielcodes sind genau 80 bits lang und beginnen immer mit '| |' und enden mit '|||'.\n
  -|Entgelts.|--Hausnummer--|----Straße----|-------Postleitzahl----------|Prüfz|-- Bedeutung
  -|8421.8421|8421.8421.8421|8421.8421.8421|01247.01247.01247.01247.01247|01247|-- Stellenwert\n: """

    try:
        code = input(prompt)
        if code == '':
            code = '10111001001111110111101111101111110110111001011100111010101101110101011110011111'
        code = Postcode(code)
        print(code.decoded)
    except:
        error_while_processing = True
    finally:
        if error_while_processing:
            print('\n\t\033[96mVersuche es noch einmal!\033[0m')
