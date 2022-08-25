from dbr import *

license_key = ""
image = r"C:\\vs_code\\QR_Scanner\\QR_Reader\\testQR.png"

BarcodeReader.init_license("t0073oQAAAHLevwmwJB5vthcpmmYdeeVgYSNGPeSmDnIofo2XI1elNbEBQ9ksL0BrLB/io8+qj9wy5ZJ1bLtddlZrb8meKy0u0kEiRg==")
reader = BarcodeReader()

try:
   text_results = reader.decode_file(image)

   if text_results != None:
      for text_result in text_results:
            print("Barcode Format : ")
            print(text_result.barcode_format_string)
            print("Barcode Text : ")
            print(text_result.barcode_text)
            print("Localization Points : ")
            print(text_result.localization_result.localization_points)
            print("Exception : ")
            print(text_result.exception)
            print("-------------")
except BarcodeReaderError as bre:
   print(bre)