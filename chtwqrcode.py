import qrcode

# 你提供的URL
url = "twqrp-39201://twqrp/webtoapp?acqBank=006&terminalId=10011001&merchantId=0062631980010" \
      "01&encQRCode=AcKSrTAGls19%2fnKMPQeUZKjT1dFK4L5LZJzxyZe55iHK%2bF41WknrdelQ" \
      "IVugMPK5dn%2b8HckdwMUzSGEWyrZej7NrAmkAc7W6VFYvnJYd5%2btgPvPRZkvtDlJTgOtk" \
      "e%2bvmYTWjbbs9uYZALZyNTWJsIggbTe1lzlTiQMBOAB5fR41DlDmQt%2fKCQwNpSiAggCx" \
      "zijVIiJdJC265CUMH8zJMld5FGX857J2Mah6Q04cJkyS2Bgsontpsw1J6UmOu4ZzawpR6Za6spfpF" \
      "hX3H0aJNQxeDQSsfnuUatWynSUH3J0Iil3fgWgViScbqLqDsJUiW0SyDA3WhLKbsrjGkYEBZpY" \
      "3iPmgBL7q5aKtVJTvgDK%2blwczJjfvYihpYc5j75E3oYQ%3d%3d&encRetURL=AXBC%2bDwt" \
      "xAD%2b1svPy75UCILT4tiSEFOKDPPGhmK0xIdBmqLsnRgKZCqw4%2f%2fNTe9OEPp0%2fmx" \
      "O6PZoAthsSmn7yrqAWGVTSCl7Ju3%2baEWQHb8X&orderNumber=QRP1234567890&verifyCo" \
      "de=947676EC47B460307036BB5BF13959C7D8F6BBC61EC980A3CD8F995F8163C83A"

# 生成QR code
img = qrcode.make(url)

# 保存QR code圖片
img.save("qrcode.png")

print("QR code已經生成並保存為qrcode.png。")
