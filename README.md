# TEKNOFEST-2025 Hedef Tespiti ve Lazerle Isaretleme Sistemi
Bu proje, OpenCV tabanlı bir bilgisayarlı görü sistemi kullanarak kameradan alınan görüntülerde daire tespiti yapar ve tespit edilen dairenin konumuna göre step motorları Arduino üzerinden kontrol eder.

Sistem, görüntüde tespit edilen dairenin üst noktasını referans alarak lazerin hedef ile hizalanmasını sağlar. Bu sayede kamera görüntüsüne göre hesaplanan konum hatası kullanılarak motorlar doğru yönde hareket ettirilir.

Projede kullanılan kontrol yöntemi Oransal Kontrol (Proportional Control – Kp) olup, hedef ile kamera merkezi arasındaki hata büyüdükçe motor hızı artırılmaktadır.

Sistemde kamera ve lazer aynı noktada konumlandırılmış olsa da aralarında yaklaşık 3 cm’lik dikey bir mesafe bulunmaktadır. Bu nedenle kamera tarafından hesaplanan referans noktası ile lazerin gerçek vurduğu nokta birebir örtüşmez.

Algoritma görüntüde tespit edilen dairenin üst noktasını referans alır. Kamera bu noktayı hedef alacak şekilde konum hatasını hesaplar. Ancak lazer kameranın yaklaşık 3 cm altında bulunduğu için lazer ışını doğrudan bu noktaya değil, üst noktanın biraz altında kalan bölgeye isabet eder.

Bu durum sistem tasarımında bilinçli olarak kullanılmıştır. Böylece kamera üst noktayı hedef aldığında, lazer fiziksel konum farkı nedeniyle dairenin merkezine yakın bir noktayı vuracak şekilde hizalanır.

Bu mesafe teorik olarak hesaplanmak yerine yaklaşık 10 metre mesafede yapılan deneme–yanılma testleri ile kalibre edilmiştir. Böylece sistem gerçek çalışma koşullarına göre ayarlanmıştır.
