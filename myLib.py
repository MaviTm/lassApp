import sqlite3 as sql
import cmath
from threading import Thread
# from threading import Thread

class dbSql():
    dbFile = None
    vt = None
    im = None
    opBol = 0
    runBol = 0

    def __int__(self):
        pass

    @classmethod
    def dbFileSet(cls, file):
        cls.dbFile = file
        return cls

    @classmethod
    def vtConnection(cls):
        if cls.opBol != 1:
            try:
                cls.vt = sql.connect(cls.dbFile)
                cls.im = cls.vt.cursor()
                cls.opBol = 1
                print("DB bağlandı", cls.opBol)
            except:
                print("db bağlanmadı")
                cls.opBol = 0
        return cls

    @classmethod
    def vtExecute(cls, sql, db=None, commit=None, close=None):
        cls.runBol = 0
        cls.vtConnection()

        if cls.opBol != 1:
            print("db bağlanmadığı için sorgu yapılmadı", cls.opBol)
            return None
        try:
            cls.im.execute(sql)
            # print("OK:", sql)
            cls.runBol = 1
        except:
            print("ÇALIŞMADI:", sql)
            cls.runBol = 0

        if commit != None:
            cls.vtCommit()
        if close != None:
            cls.vtClose()
        return cls.im.fetchall()

    @classmethod
    def vtCommit(cls):
        cls.vt.commit()
        print("db commit")
        return cls
    @classmethod
    def vtClose(cls):
        cls.opBol = 0
        cls.vt.close()
        print("db close")
        return cls

class lastikValue():
    incToMm = 25.4
    incToCm = 2.54

    baglantiMm = 40
    baglantiMin = 15
    penceAdetMmFark = 200 #lastikCap - ((baglantiMin * xMin) + (baglantiMin * bCount)) sonucu 200 ve düşükçe pencesayisinini ilk start sayisi

    xyFark = 1
    xyFarkMax = 10
    xupper = 0.1
    xMin = 62.0
    yMax = 70.0

    def __int__(self):
        self.pencex = 0
        self.pencey = 0
        self.bagadet = 0
        self.lastikcap = 0
        self.lastik = 0
        self.xboy = 0
        self.yboy = 0

    @classmethod
    def getMinBaglantiAdet(cls, lastr):
        lastikCap = cls.lastikCapi(lastr)
        pMm = cls.xMin
        pAdet = cls.baglantiMin
        a = True
        while a == True:
            sonuc = (lastikCap - ((pAdet * pMm) + (pAdet * cls.baglantiMm)))
            if sonuc < cls.penceAdetMmFark:
                a = False
            pAdet += 1
        return pAdet

    @classmethod
    def getMinBoyMm(cls):
        minp = cls.xMin
        r = {}
        x = 0
        while minp < cls.yMax:
            xyf = cls.xyFark
            while xyf < cls.xyFarkMax:
                maxp2 = (minp + xyf)
                if maxp2 > cls.yMax:
                    break
                r['a'+str(x)] = [round(minp, 1), round(maxp2, 1)]
                # print(r['a'+str(x)], '++++++++')
                x += 1

                xyf2 = cls.xyFark
                while xyf2 < cls.xyFarkMax:
                    maxp3 = (maxp2 + (xyf2 * cls.xupper))
                    if maxp3 > cls.yMax:
                        break
                    r['a'+str(x)] = [round(minp, 1), round(maxp3, 1)]
                    # print(r['a'+str(x)], '-------------------')
                    x += 1
                    xyf2 += cls.xyFark

                xyf3 = cls.xyFark
                while xyf3 < cls.xyFarkMax:
                    maxp4 = (minp + (xyf3 * cls.xupper))
                    if maxp4 > cls.yMax:
                        break
                    r['a'+str(x)] = [round(maxp4, 1), round(maxp2, 1)]
                    # print(r['a'+str(x)], '')
                    x += 1
                    xyf3 += cls.xyFark

                xyf += cls.xyFark
            # print("#########################################################################")
            minp += cls.xyFark
        print("durdu", str(len(r)), "adet")
        return r

    @classmethod
    def lastikCapi(cls, lastr):
        if type(lastr) is not list:
            l = lastr.split('x')
        else:
            l = lastr
        yanak = (cls.yuzdeOran(l[0], l[1])[0] * 2)
        cantCm = (int(l[2]) * cls.incToMm)
        return ((cantCm + yanak) * cmath.pi)

    @classmethod
    def yuzdeOran(cls, deger, yuzde):
        deger = float(deger)
        yuzde = float(yuzde)
        yuzdesi = ((deger / 100) * yuzde)
        return [yuzdesi, (deger - yuzdesi), (deger + yuzdesi)]

class lastikler():
    lastikBoylar = []
    minBoylar = []
    sqlinsertStr = """INSERT INTO oranlar (lastik, jant, lastikcap, pencey, baglanti, pencex, pboyy, bboy, pboyx, yboymm, bboymm, xboymm, palet, oran, xyfark) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
    valueCls = None
    sql = None
    appClass = None

    def __int__(self):
        pass

    @classmethod
    def setValueCls(cls, pCls):
        cls.valueCls = pCls
        return cls

    @classmethod
    def sqlSet(cls, sql):
        cls.sql = sql
        return cls

    @classmethod
    def appClassSet(cls, appCls):
        cls.appClass = appCls
        return cls

    @classmethod
    def getLastikler(cls):
        cls.lastikBoylar = cls.sql.vtExecute("SELECT * FROM lastikler")
        return cls

    @classmethod
    def insertLastik(cls, *p):
        cls.sql.vtExecute(
            cls.sqlinsertStr.format(
                p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[4], p[8], p[9], p[10], p[11], p[12], p[13], p[14]
            )
        )

    @classmethod
    def minBoySet(cls, minb=None):
        if type(minb) is dict:
            cls.minBoylar = minb
        else:
            cls.minBoylar = cls.valueCls.getMinBoyMm()
        return cls

    tblRow = 0
    @classmethod
    def verileriOlustur(cls):
        if not cls.lastikBoylar:
            cls.getLastikler()
        if not cls.lastikBoylar:
            print("lastik boyutları alınamadı program durduruldu.")
            return False

        for i in cls.lastikBoylar:
            lastikCap = cls.valueCls.lastikCapi([i[1], i[2], i[3]])
            pAdet = cls.valueCls.getMinBaglantiAdet([i[1], i[2], i[3]])
            adetler = [(pAdet - 1), pAdet, (pAdet + 1)]
            lastikolcu = str(i[1])+str(i[2])+str(i[3])
            jant = i[3]

            cls.lastikBoyData(lastikCap, adetler, lastikolcu, jant)

            # t = Thread(target=cls.lastikBoyData, args=(lastikCap, adetler, lastikolcu, jant))
            # t.start()
        if cls.appClass != None:
            cls.appClass.veriHesaplamaBitti()
        print("############### KANAL ISLEMLERIN TUMU BASLATILDI #############")
        return cls

    @classmethod
    def lastikBoyData(cls, *arg):

        lastikCap = arg[0]
        adetler = arg[1]
        lastikolcu = arg[2]
        jant = arg[3]

        for mbb in cls.minBoylar:
                minMm = cls.minBoylar[mbb][0]
                maxMm = cls.minBoylar[mbb][1]
                for adet in adetler:
                    for px in range(0, (adet + 1)):
                        yadet = px
                        xadet = (adet - px)
                        if yadet < 0 or xadet < 0:
                            continue
                        palet = ((yadet * maxMm) + (xadet * minMm) + (adet * cls.valueCls.baglantiMm))
                        yboymm = (yadet * maxMm)
                        bboymm = (adet * cls.valueCls.baglantiMm)
                        xboymm = (xadet * minMm)
                        oran = (lastikCap - palet)
                        cls.insertLastik(
                            lastikolcu, jant, lastikCap,
                            yadet, adet, xadet,
                            maxMm, cls.valueCls.baglantiMm, minMm,
                            yboymm, bboymm, xboymm,
                            palet, oran, (maxMm - minMm)
                        )
        if cls.appClass != None:
            cls.appClass.veriProgresChange(lastikolcu, " OK")
        print(lastikolcu, " işlemler bitti")

