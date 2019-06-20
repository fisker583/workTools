#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  

import xlrd
import sys 
import struct 
import os
import shutil

# reload(sys)
# sys.setdefaultencoding('utf8')

charMap = {}

def cacheCharacters(chars):
    if isinstance(chars, (str, unicode)):
        for _, ch in enumerate(chars):
            charMap[ch] = True
    pass

class ValueWriter:
    def write(self, value, force):
        pass
    def getType(self, fieldName):
        pass
    def writeCode(self, codeCB, readerCB, obj, fieldName):
        pass
    def writeReader(self, codeCB, readerCB, obj, fieldName):
        readerCB.appendLines([
            '{0}.{1} = ValueReader.Read<{2}>(br);'.format(obj, fieldName, self.getType(fieldName))
        ])
    def getReader(self, fieldName):
        pass
class IntWriter(ValueWriter):
    def write(self, value, force):
        v = 0
        if value != '':
            v = int(float(value))
        return struct.pack('i', v)
    def getType(self, fieldName):
        return 'int'
    def getReader(self, fieldName):
        return 'ValueReader.IntValueReader'
class FloatWriter(ValueWriter):
    def write(self, value, force):
        v = 0
        if value != '':
            v = float(value)
        return struct.pack('f', v)
    def getType(self, fieldName):
        return 'float'
    def getReader(self, fieldName):
        return 'ValueReader.FloatValueReader'
class StringWriter(ValueWriter):
    def write(self, value, force):
        return packString(value)
    def getType(self, fieldName):
        return 'string'
    def getReader(self, fieldName):
        return 'ValueReader.StringValueReader'
class ArrayWriter(ValueWriter):
    name = ""
    def __init__(self, t):
        self.childWriter = getWriter(t)
    def getType(self, fieldName):
        return 'IList<' + self.childWriter.getType(fieldName) + '>'
    def write(self, value, force):
        l = str(value).split(',')
        size = 0
        pack = ''
        for s in l:
            childPack = self.childWriter.write(s, False)
            if not childPack:
                break
            size += 1
            pack += childPack
        return struct.pack('i', size) + pack
    def getBaseType(self, fieldName):
        return self.childWriter.getType(fieldName)
    def writeCode(self, codeCB, readerCB, obj, fieldName):
        self.childWriter.writeCode(codeCB, readerCB, obj, fieldName)
    def writeReader(self, codeCB, readerCB, obj, fieldName):
        readerCB.appendLines([
            '{0}.{1} = ValueReader.ReadArray(br, {2});'.format(obj, fieldName, self.childWriter.getReader(fieldName))
        ])
class KVWriter(ValueWriter):
    def __init__(self, k, v):
        self.kType = k
        self.vType = v
        self.keyType = getWriter(k)
        self.valueType = getWriter(v)
    def getType(self, fieldName):
        return 'KV' + fieldName
    def writeCode(self, codeCB, readerCB, obj, fieldName):
        kvName = 'KV' + fieldName
        codeCB.appendLines([
            'public class {0} {{'.format(kvName),
            '    public {0} key;'.format(self.keyType.getType(fieldName)),
            '    public {0} value;'.format(self.valueType.getType(fieldName)),
            '}',
            
            'private static {0} Read{0}(BinaryReader br) {{'.format(kvName),
            '    if (br.ReadBoolean()) {',
            '        var kv = new {0}();'.format(kvName)
        ])

        codeCB.addIndent(2)
        self.keyType.writeReader(codeCB, codeCB, 'kv', 'key')
        self.valueType.writeReader(codeCB, codeCB, 'kv', 'value')
        codeCB.popIndent(2)

        codeCB.appendLines([
            '        return kv;',
            '    }',
            '    return null;',
            '}'
        ])
    def writeReader(self, codeCB, readerCB, obj, fieldName):
        readerCB.appendLines([
            '{0}.{1} = ReadKV{1}(br);'.format(obj, fieldName)
        ])
    def getReader(self, fieldName):
        return 'ReadKV{0}'.format(fieldName)
    def write(self, value, force):
        m = str(value).split(':')
        pack = ''
        if len(m) < 2:
            if not force:
                print('invalidate d', value)
                return
            pack += struct.pack('?', 0)
        else:
            pack += struct.pack('?', 1)
            pack += self.keyType.write(m[0], force)
            pack += self.valueType.write(m[1], force)
        return pack

writers = {
    'i':IntWriter(),
    's':StringWriter(),
    'f':FloatWriter()
}
keyWords = {
    'interface',
    'object'
}
project_path = '../../AQGY_Client'

def getSafeName(name):
    if name in keyWords:
        return '@' + name
    return name

def getWriter(t):
    if (t[0] == 'a'): #ai/ad<si>
        return ArrayWriter(t[1:])
    elif (t[0] == 'd'): # d<si>
        return KVWriter(t[2], t[3])
    return writers[t]

def packString(value):
    s = str(value)
    cacheCharacters(value)
    pack = struct.pack('{}s'.format(len(s)), s)
    return struct.pack('i', len(pack)) + pack

class CodeBuilder:
    def __init__(self):
        self.indentSize = 0
        self.str = ""

    def addIndent(self, size):
        self.indentSize += size

    def popIndent(self, size):
        self.indentSize -= size

    def getIndentStr(self):
        return "    " * self.indentSize

    def append(self, str):
        self.str += str

    def appendLines(self, lines):
        indent = self.getIndentStr()
        for line in lines:
            self.append(indent + line + "\n")

class Generator:
    def __init__(self, fileName):
        self.fileName = fileName

    def gen(self, interfaces):
        self.wb = xlrd.open_workbook("../data/xlsx/" + self.fileName + ".xlsx")
        self.bs = self.wb.sheet_by_index(0)
        
        className = self.fileName + "Info"

        c1 = className[0]
        if c1.islower():
            className = c1.upper() + className[1:]

        namespace = "config." + self.fileName
        namespace = namespace.lower()

        codeCB = CodeBuilder()
        codeCB.appendLines([
            'using System.Collections.Generic;\n'
            'using System.IO;\n'
            'using Dict;\n',
            'namespace {0} {{'.format(namespace)])
        codeCB.addIndent(1)
        if not interfaces or len(interfaces) == 0:
            codeCB.appendLines(["public partial class {0} {{".format(className)])
        else:
            codeCB.appendLines(["public partial class {0} : ".format(className)])
            for interface in interfaces:
                codeCB.append(interface)
            codeCB.append(" {")
        codeCB.addIndent(1)
        codeCB.appendLines([
            'public static void Register() {',
            '    DictManager.Register<{0}, Packer>();'.format(className),
            '}'
        ])

        readerCB = CodeBuilder()
        readerCB.addIndent(2)
        readerCB.appendLines(['class Reader : IValueReader<{0}> {{'.format(className)])
        readerCB.addIndent(1)
        readerCB.appendLines(['public {0} Read(BinaryReader br) {{'.format(className)])
        readerCB.appendLines(['    return Read(br, new {0}());'.format(className)])
        readerCB.appendLines(['}\n'])
        readerCB.appendLines(['public {0} Read(BinaryReader br, {0} obj) {{'.format(className)])
        readerCB.addIndent(1)
        uniqueIdType = 'int'
        typeRow = self.bs.row_values(1) #__type__
        if typeRow[1] == '':
            typeRow = self.bs.row_values(2) #__type__
        nameRow = self.bs.row_values(3) #__name__
        for index in range(0, len(nameRow)):
            t = typeRow[index]
            n = getSafeName(nameRow[index])
            if index == 0:
                n = 'uniqueId'
                t = typeRow[1]
            w = getWriter(t)
            type = w.getType(n)
            if index == 0:
                uniqueIdType = type
            
            #getter
            codeCB.appendLines([
                "public {0} {1} {{".format(type, n),
                "    get; private set;",
                "}"
            ])

            #reader
            w.writeCode(codeCB, readerCB, 'obj', n)
            w.writeReader(codeCB, readerCB, 'obj', n)
            
        readerCB.appendLines(['return obj;'])
        readerCB.popIndent(1)       #end read
        readerCB.appendLines(["}"])
        readerCB.popIndent(1)
        readerCB.appendLines(["}"]) #end class

        # dict packer
        readerCB.appendLines([
            'class Packer : DictPacker<{0}, {1}> {{'.format(uniqueIdType, className),
            '    protected override IValueReader<{0}> GetReader() {{'.format(className),
            '        return new Reader();',
            '    }',
            '    protected override {0} GetKey({1} v) {{'.format(uniqueIdType, className),
            '        return v.uniqueId;',
            '    }',
            '}'
        ])
        
        codeCB.popIndent(1)
        codeCB.append("\n\n")
        codeCB.append(readerCB.str)

        codeCB.appendLines(["}"])   #end class
        codeCB.popIndent(1)
        codeCB.appendLines(['}'])   #end namespace
        # print(codeCB.str)
        open(project_path + '/Assets/Scripts/Dict/' + className + ".cs", 'w').write(codeCB.str)

        # write db
        filePath = project_path + "/Assets/Config/Resources/Dict/" + className + ".bytes"
        dbFile = open(filePath, 'wb')
        # write total rows size
        dbFile.write(struct.pack('i', self.bs.nrows - 4))
        for row in range(4, self.bs.nrows):
            data = self.bs.row_values(row)
            pack = ''
            for col in range(0, len(nameRow)):
                t = typeRow[col]
                if col == 0:
                    t = typeRow[1] #uniqueId
                v = data[col]
                w = getWriter(t)
                try:
                    pack += w.write(v, True)
                except Exception as e:
                    print('    name:{0}, type:{1}, text:{2}'.format(nameRow[col], t, v))
                    print(e.message)
            # row size
            dbFile.write(struct.pack('i', len(pack)))
            # row content
            dbFile.write(pack)
        dbFile.close()
        shutil.copyfile(filePath, "../data/dict/" + className + ".bytes")
interfaceMap = {
    "Map02": ["IMapInfo"],
    "Map03": ["IMapInfo"],
    "Map04": ["IMapInfo"],
    "Dataosha": ["IMapInfo"],
    "Map05": ["IMapInfo"]
}
excludeFiles = [
    "GiftCdKey.xlsx",
    "User.xlsx",
    "Wallet.xlsx",
    "BetaGift.xlsx",
    "MaskWord.xlsx"
]
def genAll():
    for (_, _, files) in os.walk('../data/xlsx'):
        for fileName in files:
            if (fileName[0] != '~' and fileName[-5:] == '.xlsx' and not fileName in excludeFiles):
                name = fileName[0:-5]
                gen(name)
    # 生成Textmesh Pro 文字
    sb = ''
    for _, ch in enumerate(charMap.keys()):
        sb = sb + ch
    # open("text.txt", "wb").write(sb)
    
def gen(name):
    print(name)
    generator = Generator(name)
    generator.gen(interfaceMap.get(name))

#'Item', 'Character', 'Skill', 'Fashion', 'MaskWord', 'LanguageVersion', 'Buff', 'RandomName'
#'Audio', 'Growup', 'Shop', 'FashionShop', 'Rune', 'SkillLib', 'Task', 'Act', 'TaskReward', 'Config'
#'Weapon', 'Trigger', 'Survivalmap', 'FullLevelScoreFall', 'Grade', 'Bullet', 'Attribute'
#'ActivityPush', 'Avatar', 'BattleItem', 'CharacterLevUp', 'Contest', 'ControlClassBuffType'
#'CurrencyShop', 'DropLimited', 'Email', 'Experience', 'FullLevelScoreFall', 'FuncUnlock', 'Gift'
#'Index', 'Itemrefresh', 'Lottery', 'MainLottery', 'Package', 'Rank', 'RedPacket', 'RunePool', 'RuneSlot'
#'Scene', 'Season', 'SevenDays', 'Sign', 'Tips', 'Suit'
genAll()