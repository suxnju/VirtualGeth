# import requests
from lxml import etree

# URL = "https://ethervm.io/"

# res = requests.get(URL)
# ethervm = etree.HTML(res.text)
ethervm = etree.parse('C:/Users/Su/Desktop/Ethereum Virtual Machine Opcodes.html',etree.HTMLParser())

trs = ethervm.xpath("/html/body/div[2]/div/table[3]/tbody/tr")

f = open("table.py","w",encoding="utf-8")

OpcodeList = []

for tr in trs:
    tds = tr.xpath("./td")
    Opcode = tds[0].xpath("string(.)").strip()
    Mnemonic = tds[1].xpath("string(.)").strip()
    Expression = tds[-2].xpath("string(.)").strip().replace("\n","").replace(" ","")
    Notes = tds[-1].xpath("string(.)").strip()
    if Mnemonic == "Invalid":
        continue
#         format_function = """\
# def {}(self):
#     '''
#         {} \\\\
#         {} \\\\
#         {}
#     '''
#     raise ValueError('Not implement {} error!')

# """
        # f.write(format_function.format(Mnemonic,Opcode,Expression,Notes,Mnemonic))
        # f.flush()
        # print()
    f.write('\t"%s":(0x%s,"%s","%s"),\n'%(Mnemonic, Opcode, Expression, Notes))
        # OpcodeList.append(Mnemonic)
    # f.flush()

# for opcode in OpcodeList:
#     f.write("def %s(self):\n\traise ValueError('Not implement error!')\n\n"%opcode)

f.close()