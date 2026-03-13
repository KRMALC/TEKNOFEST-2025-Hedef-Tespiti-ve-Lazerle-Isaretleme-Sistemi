# TEKNOFEST 2025 Hedef Tespiti ve Lazerle İşaretleme Sistemi

Bu proje, **OpenCV tabanlı bir bilgisayarlı görü sistemi** kullanarak kameradan alınan görüntülerde daire tespiti yapar ve tespit edilen hedefin konumuna göre step motorları STM tabanlı kontrol kartı üzerinden yönlendirir.

Sistem, görüntüde tespit edilen dairenin **üst noktasını referans alır**. Kamera bu noktayı hedef alacak şekilde konum hatasını hesaplar. Hesaplanan hata bilgisine göre motorların yönü ve hızı belirlenir.

Projede kullanılan kontrol yöntemi Oransal Kontrol (Proportional Control – Kp) olup, hedef ile referans ekseni arasındaki hata büyüdükçe motor hızı artırılmaktadır..

## Çalışma Mantığı

Sistemde kamera ve lazer aynı doğrultuda konumlandırılmış olsa da aralarında yaklaşık **3 cm’lik dikey bir mesafe** bulunmaktadır. Bu nedenle kamera tarafından referans alınan nokta ile lazerin fiziksel olarak vurduğu nokta birebir aynı değildir.

Algoritma görüntüde tespit edilen dairenin **üst noktasını** esas alır. Ancak lazer, kameranın yaklaşık 3 cm altında bulunduğu için doğrudan üst noktaya değil, bu noktanın biraz altına isabet eder. Bu yapı sistem tasarımında bilinçli olarak kullanılmıştır. Böylece kamera üst noktayı referans aldığında, lazer fiziksel konum farkı nedeniyle dairenin merkezine yakın bir bölgeye hizalanmış olur.

Bu mesafe teorik hesap yerine yaklaşık 10 metre çalışma mesafesinde yapılan **deneme–yanılma** testleri ile kalibre edilmiştir. Böylece sistem gerçek kullanım koşullarına göre ayarlanmıştır.

## Notlar

- Programın çalışabilmesi için **STM ile bilgisayar arasında UART (seri haberleşme)** bağlantısının kurulmuş olması gerekir.
- Kod içerisinde tanımlanan **serial port** değerinin sisteminizde bağlı olan STM kartının portu ile aynı olması gerekir.
- Serial portun **boşta olması gerekir**.Başka bir uygulama aynı portu kullanıyorsa bağlantı kurulamaz.
- Sistemin doğru çalışabilmesi için tespit edilmek istenen dairenin **Min Radius** ve **Max Radius** değerleri sahadaki hedefe göre ayarlanmalıdır.
