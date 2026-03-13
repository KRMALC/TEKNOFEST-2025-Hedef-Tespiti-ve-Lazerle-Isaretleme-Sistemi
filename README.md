# TEKNOFEST 2025 Hedef Tespiti ve Lazerle İşaretleme Sistemi

Bu proje, **OpenCV tabanlı bir bilgisayarlı görü sistemi** kullanarak kameradan alınan görüntülerde daire tespiti yapar ve tespit edilen hedefin konumuna göre step motorları **STM tabanlı kontrol kartı** üzerinden yönlendirir.

Sistem, görüntüde tespit edilen dairenin **üst noktasını referans alır**. Kamera bu noktayı hedef alacak şekilde konum hatasını hesaplar.

## Çalışma Mantığı

Sistemde kamera ve lazer aynı doğrultuda konumlandırılmış olsa da aralarında yaklaşık **3 cm’lik dikey bir mesafe** bulunmaktadır.

## Notlar

- Programın çalışabilmesi için **STM ile bilgisayar arasında UART (seri haberleşme)** bağlantısının kurulmuş olması gerekir.
- Kod içerisinde tanımlanan **serial port** değerinin sisteminizde bağlı olan STM kartının portu ile aynı olması gerekir.
- Serial portun **boşta olması gerekir**.
- Tespit edilmek istenen dairenin **Min Radius** ve **Max Radius** değerleri doğru ayarlanmalıdır.
