try:
  HIVE = os.getenv('HIVE')
  nuke.pluginAddPath(HIVE, addToSysPath=True)

  print "\n "+chr(218)+chr(196)*37 + chr(191)+"\n "+ chr(179) + " HIVE nuke.env - loading successfull " + chr(179)+"\n "+chr(192)+chr(196)*37 + chr(217)
except:
  print "\n "+chr(218)+chr(196)*32 + chr(191)+"\n "+ chr(179) + " HIVE nuke.env - loading failed " + chr(179)+"\n "+chr(192)+chr(196)*32 + chr(217)


# just for RR
# nuke.pluginAddPath('//bigfoot/breakingpoint/_sandbox/HIVE')