# Tugas Besar 1 Strategi Algoritma - Stimanana
## Pemanfaatan Algoritma Greedy dalam Permainan Diamonds

## Kelompok Stimanana
| No. | Nama                     |    NIM    |
|:---:|:-------------------------|:---------:|
| 1.  | Kristof Tsunami Ginting  | 123140117 |
| 2.  | Mulya Delani             | 123140019 |
| 3.  | Mega Zayyani             | 123140180 |

## Daftar Isi
1. [Deskripsi Umum](#deskripsi-umum)
2. [Penjelasan Algoritma](#penjelasan-algoritma)
3. [Penggunaan Program](#penggunaan-program)

## Deskripsi Umum
Tugas Besar 1 Strategi Algoritma ini bertujuan untuk mengimplementasikan bot pada permainan _Diamonds_. Permainan _Diamonds_ merupakan permainan sederhana yang memiliki objektif bagi pemain untuk mendapatkan _Diamonds_ sebanyak-banyaknya pada papan permainan.

Bot yang dibuat akan menggunakan algoritma _**Greedy**_ dengan tujuan utama mendapatkan _Diamond_ sebanyak-banyaknya agar dapat memenangkan permainan.

## Penjelasan Algoritma
Kelompok Stimanana menggunakan beberapa strategi greedy untuk menentukan langkah selanjutnya. Berikut adalah beberapa metode utama yang diimplementasikan dalam file `Stimanana.py`:

1. **distance**: Menghitung jarak antara dua posisi menggunakan rumus jarak Manhattan.
2. **get_teleporters**: Mencari semua objek bertipe teleporter di papan permainan untuk efisiensi jarak.
3. **distance_with_teleporter**: Menghitung jarak antara dua posisi dengan mempertimbangkan penggunaan teleportasi.
4. **get_best_teleport_or_base**: Menentukan apakah lebih baik menggunakan teleportasi atau langsung menuju base.
5. **return_to_base**: Menghitung arah langkah menuju base bot.
6. **get_closest_diamond**: Mencari _Diamond_ terdekat dari posisi bot, dengan opsi untuk memilih antara _Diamond_ biasa atau _Red Diamond_.
7. **find_enemy_to_tackle**: Mencari musuh terdekat yang dapat diserang.
8. **get_red_button**: Menemukan posisi red button di papan permainan.
9. **should_press_red_button**: Menentukan apakah bot harus menekan red button berdasarkan jumlah _Diamonds_ yang dimiliki.
10. **next_move**: Fungsi utama yang menentukan langkah selanjutnya bot berdasarkan berbagai strategi greedy.

Implementasi dari algoritma tersebut dapat ditemukan di file _Stimanana.py_ pada struktur:
```
src/game/logic/Stimanana.py
```

## Penggunaan Program
Sebelum proses instalasi, pengguna harus memasang _requirements_ sebagai berikut:
- NodeJS (npm)
- Docker
- yarn

1. Clone repository ini sebagai algoritma bot yang akan digunakan
```
git clone https://github.com/Christ204/Tubes-Stigma_Stimanana-bot.git
```
2. Clone repository ini sebagai _game engine_.
```
git clone https://github.com/haziqam/tubes1-IF2211-game-engine.git
```
3. Pemain dapat menjalankan bot dengan membuat file run.bat atau run.sh
4. Kemudian untuk menjalankan keseluruhan bot dalam file tersebut, buka terminal dan jalankan perintah: 
```
./run-bots.bat
```
atau
```
chmod +x ./run-bots.sh
./run-bots.sh
```
5. Pemain dapat menjalankan bot secara manual dengan memasukkan _command_ :
```
python main.py --logic Stimanana --email=stimanana@email.com --name=stimanana --password=stimanana --team etimo
```
